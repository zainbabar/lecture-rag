# load the experiment files and turn chunks into searchable text

import argparse
import json
from pathlib import Path

from .chunk import add_search_text, chunk_markdown

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "evaluation/retrieval-eval-set.json"
DEFAULT_CONTEXT = ROOT / "search_context.json"


# load the selected lectures and add reviewed assumptions to each unit
def prepare_corpus(dataset: dict, context: dict) -> list[dict]:
    excluded = dataset["corpus"]["exclude_chunk_types"]
    chunks = []

    # use the explicit file list, not every file that happens to be in lectures/
    for name in dataset["corpus"]["files"]:
        file_chunks = chunk_markdown(ROOT / name)
        add_search_text(file_chunks, context["chunk_assumptions"], context["global_assumptions"])
        for chunk in file_chunks:
            if chunk["type"] not in excluded:
                chunks.append(chunk)

    # catch labels pointing at chunks we aren't actually searching
    known_ids = [chunk["id"] for chunk in chunks]
    for question in dataset["questions"]:
        for gold_id in question["gold_chunk_ids"]:
            if gold_id not in known_ids:
                raise ValueError(
                    f"{question['id']} has a gold id that isn't in the corpus: {gold_id}"
                )
    return chunks


# return the eval set + searchable chunks, without loading any models
def prepare_experiment(dataset_path: Path = DEFAULT_DATASET) -> tuple[dict, list[dict]]:
    dataset = json.loads(dataset_path.read_text())
    context = json.loads(DEFAULT_CONTEXT.read_text())
    return dataset, prepare_corpus(dataset, context)


def main() -> None:
    parser = argparse.ArgumentParser(description="Load the corpus and check the eval labels.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()

    dataset, chunks = prepare_experiment(args.dataset)
    answerable = sum(q["answerable"] for q in dataset["questions"])
    unanswerable = len(dataset["questions"]) - answerable
    print(
        f"{len(chunks)} searchable chunks; {len(dataset['questions'])} questions "
        f"({answerable} answerable, {unanswerable} unanswerable)."
    )


if __name__ == "__main__":
    main()
