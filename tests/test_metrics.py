import pytest

from lecture_rag.metrics import recall_at_k


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
