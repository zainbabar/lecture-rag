# Lecture RAG

A RAG study assistant over MATH 235 notes. We will compare dense, BM25, and hybrid retrieval, measure their results, then add grounded answers and a LangGraph workflow.

Corpus conversion, chunking, searchable-text assembly, and eval plumbing are ready. There are no embeddings, retrievers, metric implementations, or measured retrieval results yet.

## Setup and checks

Uses Python 3.12, `uv`, and a local `.venv`:

```sh
uv sync --locked
uv run python prepare.py
uv run pytest -q
```

Dependencies are locked in `uv.lock`: NumPy for vector search, rank-bm25 for the sparse baseline, langgraph/langchain-core for later work, pytest/Ruff for checks, and PyMuPDF for source review. No embedding model or LLM provider has been chosen.

## How the files connect

1. `lecture-pdfs/` holds the unchanged originals. `lectures/` holds their reviewed Markdown conversions: 11 lectures and three practice files. Local conversion helpers are excluded from Git.
2. `chunk.py` splits numbered units into dictionaries with original text, metadata, stable IDs, a context prefix, and preserved intro text. `add_search_text` adds a separate field without changing the body.
3. `search_context.json` holds reviewed assumptions: the course's R/C field convention and `dim(V)=n` for the Lecture 6 units that need it. We don't automatically paste the whole intro into each chunk.
4. `prepare.py` reads the eval file's explicit corpus list, chunks those files, adds searchable text, filters intro entries, and validates IDs. The current experiment uses 75 numbered units in Lectures 1–7. It never indexes the eval answers.
5. `evaluation/retrieval-eval-set.json` holds 30 development questions and gold IDs: 28 answerable, two unanswerable. See `evaluation/README.md` for the readable version. The original nine-question seed set is preserved separately.
6. `evaluate.py` accepts a retriever, passes each question to it, checks the returned IDs, and saves rankings. Optional user-written metric functions provide scores. It does not implement retrieval or recall/MRR itself.

`search_text` is: context prefix + field convention + relevant unit assumptions + original body. IDs and metadata remain separate fields. Intro entries aren't indexed independently. Stable IDs describe the source unit; content fingerprints detect changes to the experiment inputs.

## Prepare the inputs

```sh
uv run python prepare.py
uv run python prepare.py --output artifacts/chunks.json
```

The export preserves chunk order and metadata for linking future embedding rows back to chunks. Generated artifacts are ignored by Git. The original seed experiment is also available:

```sh
uv run python prepare.py --dataset evaluation/retrieval-check-set.json
```

## Plug in a retriever later

A retriever module supplies `build_retriever(chunks)`, returning a function `search(question, k)` that returns up to `k` unique chunk ID strings, best first. Build the index once in the factory; questions never receive gold labels.

Once that module exists:

```sh
uv run python evaluate.py --retriever dense:build_retriever --output artifacts/dense-rankings.json
```

`dense.py` does not exist yet. Later, `--metrics metrics:build_metrics` can supply named functions with the signature `(ranked_ids, gold_ids, k) -> float`. Without metrics, the runner saves rankings only. Unanswerable questions remain in the report but are excluded from retrieval metric averages.

The seed set keeps its original primary-source targets. Expanded multi-source questions list all designated evidence chunks. These are development labels, not exhaustive relevance judgments or a held-out test set. Record label changes before comparisons; don't claim generalization from repeated tuning on these questions.

## Supporting files

- `tests/test_plumbing.py` checks scope, body preservation, gold IDs, and runner boundaries; it doesn't test search quality.
- `docs/corpus-audit.md` records conversion corrections and unresolved source issues.

The tests check preparation and runner behavior. They are not a retrieval benchmark or proof that the math contains no mistakes.

## Next

Choose an embedding model, implement NumPy cosine ranking, then add retrieval metrics.
