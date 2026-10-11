"""Run a supplied retriever on the eval questions and save its rankings."""

import argparse
import importlib
import json
from collections.abc import Callable
from pathlib import Path

from prepare import DEFAULT_CONTEXT, DEFAULT_DATASET, fingerprint, prepare_experiment

# the retriever only sees the question + k; gold IDs never go into search
Retriever = Callable[[str, int], list[str]]
Metric = Callable[[list[str], list[str], int], float]


def run_evaluation(
    dataset: dict,
    chunks: list[dict],
    retrieve: Retriever,
    k: int = 3,
    metrics: dict[str, Metric] | None = None,
) -> dict:
    if k < 1:
        raise ValueError("k must be positive")
    known = {c["id"] for c in chunks}
    rows = []
    for question in dataset["questions"]:
        ranking = retrieve(question["question"], k)
        # reject bad output here instead of letting it skew the metrics
        if not isinstance(ranking, list) or not all(isinstance(cid, str) for cid in ranking):
            raise ValueError("Retriever must return a list of chunk ID strings")
        if len(ranking) > k or len(ranking) != len(set(ranking)):
            raise ValueError(f"Too many results or duplicate IDs: {question['id']}")
        if not set(ranking) <= known:
            raise ValueError(f"Retriever returned unknown IDs: {question['id']}")

        # keep unanswerable rankings for later abstention analysis, but don't score them
        scores = {}
        if question["score_retrieval"] and metrics:
            for name, metric in metrics.items():
                scores[name] = float(metric(ranking, question["gold_chunk_ids"], k))
        rows.append(
            {
                "question_id": question["id"],
                "question": question["question"],
                "bucket": question.get("bucket", "seed"),
                "answerable": question["answerable"],
                "gold_chunk_ids": question["gold_chunk_ids"],
                "supporting_chunk_ids": question["supporting_chunk_ids"],
                "retrieved_chunk_ids": ranking,
                "scores": scores,
            }
        )

    # metric functions do the maths; this just averages per-question scores
    scored = [row for row in rows if row["answerable"]]
    means = (
        {name: sum(row["scores"][name] for row in scored) / len(scored) for name in (metrics or {})}
        if scored
        else {}
    )
    return {
        "k": k,
        "corpus_fingerprint": fingerprint(chunks),
        "dataset_fingerprint": fingerprint(dataset),
        "question_count": len(rows),
        "scored_question_count": len(scored) if metrics else 0,
        "metric_means": means,
        "results": rows,
    }


def load_callable(spec: str) -> Callable:
    # e.g. 'my_retriever:build' means import my_retriever and get its build function
    module_name, function_name = spec.split(":", 1)
    function = getattr(importlib.import_module(module_name), function_name)
    if not callable(function):
        raise ValueError(f"{spec} is not callable")
    return function


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument(
        "--retriever",
        required=True,
        help="module:factory; factory(chunks) returns search(question, k)",
    )
    parser.add_argument(
        "--metrics", help="module:factory; factory() returns named metric functions"
    )
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    dataset, chunks = prepare_experiment(args.dataset, args.context)
    # factories do setup once and give us functions to use across all questions
    retrieve = load_callable(args.retriever)(chunks)
    metrics = load_callable(args.metrics)() if args.metrics else None
    report = run_evaluation(dataset, chunks, retrieve, args.k, metrics)
    report["retriever"] = args.retriever
    report["metric_provider"] = args.metrics
    # keep individual rankings too, so we can inspect failures after the run
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Saved rankings for {report['question_count']} questions.")
    if not metrics:
        print("No metric functions supplied; no retrieval scores were computed.")


if __name__ == "__main__":
    main()
