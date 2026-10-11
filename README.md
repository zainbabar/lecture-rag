# Lecture RAG

A study assistant over my MATH 235 lecture notes. It finds relevant passages and sends them to a local LLM, which answers with chunk-ID citations or says the notes aren't enough.

I'm building this to learn how to measure and debug RAG. Dense search, BM25, weighted hybrid search, and the baseline answer flow work. I haven't added LangGraph yet; first I want to check which failures a retry or an evidence check could fix.

## Results so far

The experiment searches 75 numbered chunks from Lectures 1–7. There are 30 development questions: 28 answerable and two unanswerable.

| Retriever | Recall@1 | Recall@3 | Recall@5 |
| --- | ---: | ---: | ---: |
| Dense | 60.7% | 76.2% | 84.5% |
| BM25 | 26.8% | 46.4% | 55.4% |
| Hybrid, equal weights | 41.1% | 70.8% | 90.5% |
| Hybrid, 75% dense weight | 44.6% | 70.8% | 91.7% |

These are October 10 local results. The 75% dense-weight hybrid was rerun on the GX10 on October 11 and reproduced the same numbers. Recall is computed per question, then averaged over the 28 answerable questions.

Dense ranks the direct answer better near the top. Hybrid finds more labelled evidence within five results, but sometimes pushes related passages above the answer. BM25 lowercases the text and splits on whitespace, so punctuation and math notation can get in the way of matching.

I tuned weights on these same questions, so I still need a held-out set. The gold IDs list the passages I chose as evidence; other passages can also answer a question. Recall measures how much of that labelled evidence search finds. I check generated answers separately.

## Baseline answers

The first 30-answer run was checked against the current chunk texts using the retrieved IDs:

- The model said it lacked evidence for both unanswerable questions.
- It also couldn't answer Q13. Search missed the definition of `[v]_B` and how reordering a basis changes coordinates.
- Every source ID mentioned in an answer was retrieved, but nine answers used plain IDs rather than the requested bracket citations.
- Q18 added an explanation absent from its evidence. Q29 needed to say that coordinate entries depend on an ordered basis.

The run saved IDs without passage snapshots, so the review used the current corpus. It checked individual answers without assigning an accuracy score.

## Run it

Python 3.12, [uv](https://docs.astral.sh/uv/), and Ollama. The current machine is a GX10 with an NVIDIA GB10 GPU; embedding setup also supports CPU and Apple Silicon.

```sh
uv sync --locked
uv run python -m lecture_rag.prepare
uv run pytest -q
uv run ruff check .
```

Download the embedding model once into the project cache:

```sh
uv run python -c 'from lecture_rag.dense import EMBEDDING_MODEL, MODEL_CACHE; from sentence_transformers import SentenceTransformer; SentenceTransformer(EMBEDDING_MODEL, cache_folder=str(MODEL_CACHE))'
```

The scripts load the cached model without downloading it again. Sentence Transformers picks the device automatically; set `LECTURE_RAG_DEVICE=cpu`, `cuda`, or `mps` to override it.

```sh
uv run python -m lecture_rag.dense
uv run python -m lecture_rag.sparse
uv run python -m lecture_rag.hybrid
```

These print Recall@1, @3, and @5. Hybrid fuses ten candidates from each retriever with a dense weight of 0.75 and RRF constant of 60. Embeddings and BM25 are built once per run; embeddings aren't persisted yet.

For generation, start Ollama and download the model:

```sh
ollama serve
# in another terminal; skip serve if Ollama is already running
ollama pull qwen3.6:35b-a3b
uv run python -m lecture_rag.rag --output artifacts/baseline-answers.json
```

`rag.py` answers all 30 questions and saves JSON with the answers, full retrieved passages, settings, and hashes of the corpus and dataset. The prompt asks for evidence-only answers and citations. The answer review above shows where it still slips. Set `OLLAMA_URL` to override the default `http://127.0.0.1:11434/api/chat` endpoint.

Generation uses `think=False`, `stream=False`, temperature 0, and `num_batch=2048`. Ollama crashed on longer prompts on this GB10; changing the batch size made the same request pass twice after fresh model loads. A [similar upstream report](https://github.com/ollama/ollama/issues/17434) describes the failure. I haven't traced it to an exact CUDA kernel.

## Code and data

```text
src/lecture_rag/   Python package: parsing, retrieval, evaluation, generation
tests/            Unit and integration checks
evaluation/       Questions, gold labels, and source verification
lectures/         Converted notes
lecture-pdfs/     Original PDFs
```

- `src/lecture_rag/chunk.py` / `prepare.py`: split numbered lecture units, attach source metadata and checked assumptions, validate the corpus and labels.
- `dense.py` / `sparse.py` / `hybrid.py`: NumPy cosine ranking, BM25, and weighted reciprocal rank fusion.
- `rag.py`: collect evidence, build the prompt, call Ollama, and export answers.
- `evaluate.py`: reusable ranking/metric runner. The retrieval scripts still use their own eval loops.
The tests check corpus loading, eval wiring, and generation requests with mocked HTTP responses. Answer quality needs its own review. The converted corpus has 11 lectures and three practice files; the experiment indexes Lectures 1–7.

Each chunk keeps its original body and a `search_text` containing the lecture prefix, reviewed assumptions, and body. Lecture intros, trailing Source checks, practice files, and eval material stay out of the index. Source corrections and unresolved issues are recorded in each lecture's Source checks section.

## Next

Inspect Q13's dense, BM25, and hybrid rankings to find where the coordinate definition gets lost. MRR, held-out questions, and measured LangGraph comparisons are still pending.
