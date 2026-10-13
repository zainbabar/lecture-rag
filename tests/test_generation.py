# check the Ollama boundary without loading models or calling the server

import io
import json
from urllib.error import HTTPError

import pytest

from lecture_rag.rag import generate_answer


def test_batch_export_preserves_evidence(monkeypatch, tmp_path):
    from lecture_rag import rag

    question = {"id": "Q01", "question": "What is a vector space?"}
    chunks = [{"id": "lecture-01-unit-1.1", "search_text": "Vector space axioms."}]
    passages = [{"id": chunks[0]["id"], "passage": chunks[0]["search_text"], "rank": 1}]
    output = tmp_path / "results" / "answers.json"
    monkeypatch.setattr("sys.argv", ["rag.py", "--output", str(output)])
    monkeypatch.setattr(rag, "load_embedding_model", lambda: object())
    monkeypatch.setattr(
        rag, "prepare_experiment", lambda *args: ({"questions": [question]}, chunks)
    )
    monkeypatch.setattr(rag, "embed_chunks", lambda chunks, model: [])
    monkeypatch.setattr(rag, "BM25Okapi", lambda tokens: object())
    monkeypatch.setattr(rag, "answer_question", lambda *args: ("An answer.", passages))

    rag.main()

    report = json.loads(output.read_text())
    # timing changes every run, so just check it's there
    assert isinstance(report["results"][0].pop("seconds"), float)
    assert isinstance(report["total_seconds"], float)
    assert report["results"] == [
        {
            "question_id": "Q01",
            "question_text": question["question"],
            "answer": "An answer.",
            "retrieved_passages": passages,
        }
    ]
    assert report["corpus_fingerprint"] == rag.fingerprint(chunks)
    assert report["dataset_fingerprint"] == rag.fingerprint({"questions": [question]})


def test_request_and_completed_answer(monkeypatch):
    question = {"question": "What is a vector space?", "gold_chunk_ids": ["not-for-the-prompt"]}
    passages = [{"id": "lecture-01-unit-1.1", "passage": "Vector space axioms.", "rank": 1}]

    def respond(request, timeout):
        payload = json.loads(request.data)
        assert payload["options"] == {"temperature": 0, "num_batch": 2048}
        assert payload["stream"] is False and payload["think"] is False
        assert request.get_method() == "POST"
        prompt = payload["messages"][1]["content"]
        assert question["question"] in prompt
        assert passages[0]["id"] in prompt and passages[0]["passage"] in prompt
        assert "not-for-the-prompt" not in prompt
        return io.BytesIO(
            json.dumps(
                {
                    "done": True,
                    "done_reason": "stop",
                    "message": {"content": "The axioms apply [lecture-01-unit-1.1]."},
                }
            ).encode()
        )

    monkeypatch.setattr("lecture_rag.rag.urllib.request.urlopen", respond)
    assert generate_answer(question, passages, "http://localhost/api/chat").endswith(
        "[lecture-01-unit-1.1]."
    )


def test_server_error_keeps_ollama_detail(monkeypatch):
    def fail(request, timeout):
        raise HTTPError(
            request.full_url,
            500,
            "Internal Server Error",
            {},
            io.BytesIO(b'{"error":"CUDA illegal memory access"}'),
        )

    monkeypatch.setattr("lecture_rag.rag.urllib.request.urlopen", fail)
    with pytest.raises(RuntimeError, match="Ollama HTTP 500:.*CUDA illegal memory access"):
        generate_answer({"question": "Hello"}, [], "http://localhost/api/chat")


@pytest.mark.parametrize(
    "response",
    [
        {"done": False},
        {"done": True, "done_reason": "length"},
        {"done": True, "message": {"content": " "}},
    ],
)
def test_unfinished_or_empty_answers_are_errors(monkeypatch, response):
    monkeypatch.setattr(
        "lecture_rag.rag.urllib.request.urlopen",
        lambda request, timeout: io.BytesIO(json.dumps(response).encode()),
    )
    with pytest.raises(RuntimeError):
        generate_answer({"question": "Hello"}, [], "http://localhost/api/chat")
