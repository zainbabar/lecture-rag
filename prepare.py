"""Load the experiment files and turn chunks into searchable text."""

import argparse
import hashlib
import json
from chunk import add_search_text, chunk_markdown
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "evaluation/retrieval-eval-set.json"
DEFAULT_CONTEXT = ROOT / "search_context.json"


def load_dataset(path: Path) -> dict:
    """Load the questions and catch label/setup mistakes before running search."""
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported eval schema version")
    files = data["corpus"]["files"]
    questions = data["questions"]
    if not files or len(files) != len(set(files)):
        raise ValueError("Corpus files must be nonempty and unique")
    if not questions:
        raise ValueError("The eval set has no questions")
    seen = set()
    for question in questions:
        qid = question["id"]
        if qid in seen or not question["question"].strip():
            raise ValueError(f"Duplicate ID or empty question: {qid}")
        seen.add(qid)
        gold = question["gold_chunk_ids"]
        if len(gold) != len(set(gold)):
            raise ValueError(f"Duplicate gold IDs: {qid}")
        # this dataset uses gold ids for answerable questions, [] for unanswerable
        if question["answerable"] != bool(gold):
            raise ValueError(f"Answerability and gold IDs disagree: {qid}")
        if question["score_retrieval"] != question["answerable"]:
            raise ValueError(f"Unanswerable questions must stay out of retrieval metrics: {qid}")
    return data


def prepare_corpus(
    dataset: dict, root: Path = ROOT, context_path: Path = DEFAULT_CONTEXT
) -> list[dict]:
    """Load the chosen lectures and add checked context to their numbered units."""
    context = json.loads(context_path.read_text())
    if context.get("schema_version") != 1:
        raise ValueError("Unsupported context schema version")
    assumptions = context["chunk_assumptions"]
    chunks = []
    excluded = set(dataset["corpus"]["exclude_chunk_types"])
    if "intro" not in excluded:
        raise ValueError("Intro entries are context, not indexed units in this experiment")

    # use the explicit file list, not every file that happens to be in lectures/
    for name in dataset["corpus"]["files"]:
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError(f"Corpus file is outside the project: {name}")
        file_chunks = chunk_markdown(path)
        add_search_text(file_chunks, assumptions, context["global_assumptions"])
        chunks.extend(c for c in file_chunks if c["type"] not in excluded)

    ids = [c["id"] for c in chunks]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Prepared chunk IDs must be nonempty and unique")
    known = set(ids)
    # catch labels pointing at chunks we aren't actually searching
    for question in dataset["questions"]:
        referenced = question["gold_chunk_ids"] + question["supporting_chunk_ids"]
        if not set(referenced) <= known:
            raise ValueError(f"Gold/supporting IDs outside corpus: {question['id']}")
    for chunk in chunks:
        if not chunk["text"].strip() or not chunk["search_text"].strip():
            raise ValueError(f"Empty chunk: {chunk['id']}")
    return chunks


def fingerprint(value: object) -> str:
    # same inputs -> same hash; useful for checking we compared the same experiment
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def prepare_experiment(
    dataset_path: Path = DEFAULT_DATASET, context_path: Path = DEFAULT_CONTEXT, root: Path = ROOT
) -> tuple[dict, list[dict]]:
    """Return the eval set + searchable chunks, without loading any models."""
    dataset = load_dataset(dataset_path)
    return dataset, prepare_corpus(dataset, root, context_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument(
        "--output", type=Path, help="Optional JSON export, e.g. artifacts/chunks.json"
    )
    args = parser.parse_args()
    dataset, chunks = prepare_experiment(args.dataset, args.context)
    if args.output:
        # save the exact prepared corpus + hashes so later runs can be compared
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(
                {
                    "corpus_fingerprint": fingerprint(chunks),
                    "dataset_fingerprint": fingerprint(dataset),
                    "chunks": chunks,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
    answerable = sum(q["answerable"] for q in dataset["questions"])
    print(
        f"{len(chunks)} searchable chunks; {len(dataset['questions'])} questions "
        f"({answerable} answerable, {len(dataset['questions']) - answerable} unanswerable)."
    )
    print("Inputs validated. No embeddings or retrieval results have been generated.")


if __name__ == "__main__":
    main()
