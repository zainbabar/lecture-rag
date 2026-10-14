# checks for corpus/eval wiring. These aren't retrieval-quality tests

import json

import pytest

from lecture_rag.prepare import ROOT, prepare_corpus, prepare_experiment

DATASETS = [
    "evaluation/retrieval-eval-set.json",
    "evaluation/heldout-eval-set.json",
    "evaluation/test-eval-set.json",
]


def test_corpus_size_and_ids():
    dataset, chunks = prepare_experiment()
    ids = [chunk["id"] for chunk in chunks]
    assert len(chunks) == 75
    assert len(set(ids)) == 75
    assert len(dataset["questions"]) == 30


def test_search_text_keeps_the_body():
    _, chunks = prepare_experiment()
    for chunk in chunks:
        # intro entries stay out of the index
        assert chunk["type"] != "intro"
        # prefix comes first, original body comes last
        assert chunk["search_text"].startswith(chunk["context_prefix"])
        assert chunk["search_text"].endswith(chunk["text"].strip())


def test_checked_assumption_is_added():
    _, chunks = prepare_experiment()
    for chunk in chunks:
        if chunk["id"] == "lecture-06-unit-6.1":
            assert "dim(V)=n" in chunk["search_text"]


@pytest.mark.parametrize("path", DATASETS)
def test_gold_ids_exist_in_corpus(path):
    # prepare_experiment raises if a gold id isn't in the corpus
    dataset, chunks = prepare_experiment(ROOT / path)
    assert len(chunks) == 75
    for question in dataset["questions"]:
        assert question["answerable"] == (len(question["gold_chunk_ids"]) > 0)


def test_bad_gold_id_raises():
    dataset, _ = prepare_experiment()
    dataset["questions"][0]["gold_chunk_ids"] = ["lecture-08-unit-8.1"]
    context = json.loads((ROOT / "search_context.json").read_text())
    with pytest.raises(ValueError):
        prepare_corpus(dataset, context)
