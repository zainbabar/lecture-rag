# checks for corpus/eval wiring. These aren't retrieval-quality tests

import copy
import json
import re

import pytest

from lecture_rag.chunk import chunk_files
from lecture_rag.prepare import ROOT, load_dataset, prepare_corpus, prepare_experiment


def test_scope_and_original_bodies():
    dataset, chunks = prepare_experiment()
    assert len(chunks) == 75
    assert {c["lecture"] for c in chunks} == set(range(1, 8))
    originals = {c["id"]: c for f in chunk_files()[1] for c in f["data"]}
    for chunk in chunks:
        assert chunk["type"] != "intro"
        assert chunk["text"] == originals[chunk["id"]]["text"]
        assert chunk["search_text"].endswith(chunk["text"].strip())
        assert "**Source:**" not in chunk["search_text"]
        assert "## Source checks" not in chunk["search_text"]
        assert chunk["search_text"].startswith(chunk["context_prefix"])
        source = (ROOT / "lectures" / chunk["source_file"]).read_text()
        body = re.search(re.escape(chunk["heading"]) + r"\n([\s\S]*?)(?=^#|\Z)", source, re.M)
        assert body and body[1] == chunk["text"]
    theorem = next(c for c in chunks if c["id"] == "lecture-06-unit-6.1")
    assert "dim(V)=n" in theorem["search_text"]
    assert len(dataset["questions"]) == 30


def test_seed_labels_stay_the_same():
    seed = load_dataset(ROOT / "evaluation/retrieval-check-set.json")
    expanded, _ = prepare_experiment()
    for old, new in zip(seed["questions"], expanded["questions"]):
        for key in ("id", "question", "gold_chunk_ids", "supporting_chunk_ids", "answerable"):
            assert new[key] == old[key]


def test_bad_gold_id_is_rejected():
    dataset, _ = prepare_experiment()
    dataset["questions"][0]["gold_chunk_ids"] = ["lecture-08-unit-8.1"]
    with pytest.raises(ValueError, match="outside corpus"):
        prepare_corpus(dataset)


def test_duplicate_question_is_rejected(tmp_path):
    dataset, _ = prepare_experiment()
    dataset["questions"].append(copy.deepcopy(dataset["questions"][0]))
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(dataset))
    with pytest.raises(ValueError, match="Duplicate ID"):
        load_dataset(path)
