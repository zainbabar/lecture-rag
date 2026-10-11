# Lecture RAG

A study assistant over my MATH 235 lecture notes. It retrieves relevant passages, sends them to a local LLM, and asks for an answer with chunk-ID citations or an abstention if the notes aren't enough.

I'm building this to learn how to measure and debug RAG. Dense search, BM25, weighted hybrid search, and a baseline answer flow work. LangGraph is next, once there's a failure that gives it a reason to exist.

## Results so far

The experiment searches **75 numbered chunks from Lectures 1–7**, using 30 development questions: 28 answerable and two unanswerable.

| Retriever | Recall@1 | Recall@3 | Recall@5 |
| --- | ---: | ---: | ---: |
| Dense | 60.7% | 76.2% | 84.5% |
| BM25 | 26.8% | 46.4% | 55.4% |
| Hybrid, equal weights | 41.1% | 70.8% | 90.5% |
| Hybrid, 75% dense weight | 44.6% | 70.8% | 91.7% |

These are October 10 local results. The 75% dense-weight hybrid was rerun on the GX10 on October 11 and reproduced the same numbers. Recall is computed per question, then averaged over the 28 answerable questions.

Dense ranks the direct answer better near the top. Hybrid finds more labelled evidence within five results, but sometimes pushes related passages above the answer. BM25 uses lowercase + whitespace tokenization, so punctuation and math notation can make matching brittle.

I tuned weights on this development set. These aren't held-out results, and gold IDs are designated evidence targets rather than an exhaustive list of every valid passage. Retrieval recall also doesn't measure whether the generated answer is correct.

## Baseline answers

The first 30-answer run was manually checked against the retrieved chunk texts:

- Both unanswerable questions triggered abstention.
- One answerable question, Q13, also triggered abstention: search missed the definition of `[v]_B` and basis reordering.
- Every source ID mentioned in an answer was retrieved, but nine answers used plain IDs rather than the requested bracket citations.
- Q18 added an explanation absent from its evidence. Q29 needed to state explicitly that coordinate entries depend on an ordered basis.

That's a manual review of this development set, not an answer-accuracy score or a held-out result.

## Run it

Python 3.12, [uv](https://docs.astral.sh/uv/), and Ollama. The current machine is a GX10 with an NVIDIA GB10 GPU; embedding setup also supports CPU and Apple Silicon.

```sh
uv sync --locked
uv run python prepare.py
uv run pytest -q
uv run ruff check .
```

Download the embedding model once into the project cache:

```sh
uv run python -c 'from dense import EMBEDDING_MODEL, MODEL_CACHE; from sentence_transformers import SentenceTransformer; SentenceTransformer(EMBEDDING_MODEL, cache_folder=str(MODEL_CACHE))'
```

The scripts load the cached model without downloading it again. Sentence Transformers picks the device automatically; set `LECTURE_RAG_DEVICE=cpu`, `cuda`, or `mps` to override it.

```sh
uv run python dense.py
uv run python sparse.py
uv run python hybrid.py
```

These print Recall@1, @3, and @5. Hybrid fuses ten candidates from each retriever with a dense weight of 0.75 and RRF constant of 60. Embeddings and BM25 are built once per run; embeddings aren't persisted yet.

For generation, start Ollama and download the model:

```sh
ollama serve
# in another terminal; skip serve if Ollama is already running
ollama pull qwen3.6:35b-a3b
uv run python rag.py --output artifacts/baseline-answers.json
```

`rag.py` answers all 30 questions and saves JSON with the answers, full retrieved passages, settings, and corpus/dataset fingerprints. The prompt requires evidence-only answers and citations, but those rules still need checking. Set `OLLAMA_URL` to override the default `http://127.0.0.1:11434/api/chat` endpoint.

Generation uses `think=False`, `stream=False`, temperature 0, and `num_batch=2048`. The batch setting works around a reproducible CUDA crash with longer prompts on this GB10. The original failing request passed twice from fresh model loads after that change; see the [upstream report](https://github.com/ollama/ollama/issues/17434). The exact kernel failure hasn't been diagnosed here.

## Code and data

- `chunk.py` / `prepare.py`: split numbered lecture units, attach source metadata and checked assumptions, validate the corpus and labels.
- `dense.py` / `sparse.py` / `hybrid.py`: NumPy cosine ranking, BM25, and weighted reciprocal rank fusion.
- `rag.py`: collect evidence, build the prompt, call Ollama, and export answers.
- `evaluate.py`: reusable ranking/metric runner. The retrieval scripts still use their own eval loops.
- `evaluation/`: development questions and labels, plus the original nine-question check set.
- `tests/`: corpus/eval wiring and mocked generation requests. These don't measure answer quality.
- `lectures/` / `lecture-pdfs/`: converted notes and original source PDFs. The full conversion has 11 lectures and three practice files; only Lectures 1–7 are indexed.

Each chunk keeps its original body and a `search_text` containing the lecture prefix, reviewed assumptions, and body. Lecture intros, trailing Source checks, practice files, and eval material stay out of the index. Source corrections and unresolved issues are recorded in each lecture's Source checks section.

## Next

Inspect Q13's dense, BM25, and hybrid rankings to find where the coordinate definition gets lost. MRR, held-out questions, and measured LangGraph comparisons are still pending.
