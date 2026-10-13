import pytest

from lecture_rag.metrics import mrr, recall_at_k, reciprocal_rank_at_k


@pytest.mark.parametrize(
    "retrieved, gold, k, expected",
    [
        (["a", "b", "c"], ["a", "c"], 2, 0.5),  # one of two gold ids in top 2
        (["a", "b", "c"], ["a", "c"], 3, 1.0),  # both found in top 3
        (["a", "b", "c"], ["d"], 3, 0.0),  # no gold hit
    ],
)
def test_recall_at_k(retrieved, gold, k, expected):
    assert recall_at_k(retrieved, gold, k) == expected


@pytest.mark.parametrize(
    "retrieved, gold, k, expected",
    [
        (["a", "b", "c"], ["a"], 3, 1.0),  # first result is gold
        (["a", "b", "c"], ["b", "c"], 3, 0.5),  # only the first hit counts
        (["a", "b", "c"], ["c"], 2, 0.0),  # gold is outside the cutoff
        (["a", "b"], ["c"], 5, 0.0),  # no hit even with a larger cutoff
        ([], ["a"], 5, 0.0),  # no results
    ],
)
def test_reciprocal_rank_at_k(retrieved, gold, k, expected):
    assert reciprocal_rank_at_k(retrieved, gold, k) == expected


def test_mrr():
    # ranks 1, 2, and no hit: (1 + 0.5 + 0) / 3 = 0.5
    retrieved = [["a", "b"], ["x", "b"], ["x", "y"]]
    gold = [["a"], ["b"], ["c"]]
    assert mrr(retrieved, gold, k=5) == 0.5
    # at cutoff 1, only the first question gets a hit
    assert mrr(retrieved, gold, k=1) == pytest.approx(1 / 3)
