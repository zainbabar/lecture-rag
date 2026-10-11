# Lecture RAG

A study assistant over my MATH 235 lecture notes. It finds relevant passages and sends them to a local LLM, which answers with chunk-ID citations or says the notes aren't enough.

I'm building this to learn how to measure and debug RAG. Dense search, BM25, weighted hybrid search, a baseline answer flow, and a LangGraph version with an evidence check and one query rewrite all work.

What I found so far:

- Dense search beats BM25 on these notes. Weighted hybrid looked best on my 30 dev questions (91.7% Recall@5), but on 16 held-out questions it tied dense at 76.9%. Part of that dev gain came from tuning on the same questions.
- Math notation causes most retrieval misses. Questions like "what does `[v]_B` mean" never say "coordinate vector", which is how the notes phrase it.
- The LangGraph evidence check plus one query rewrite fixed Q13 on the dev set. On the held-out set it fixed one question and broke two, because the checker rejected passages the model could have answered from.
- Both versions abstained on all five unanswerable questions.

Setup and commands are in [Run it](#run-it).

## Results so far

The experiment searches 75 numbered chunks from Lectures 1–7. There are 30 development questions: 28 answerable and two unanswerable.

| Retriever | Recall@1 | Recall@3 | Recall@5 |
| --- | ---: | ---: | ---: |
| Dense | 60.7% | 76.2% | 84.5% |
| BM25 | 26.8% | 46.4% | 55.4% |
| Hybrid, equal weights | 41.1% | 70.8% | 90.5% |
| Hybrid, 75% dense weight | 44.6% | 70.8% | 91.7% |

I first ran these on my Mac, then reran the 75% dense-weight hybrid on the GX10 and got the same numbers. Recall is computed per question, then averaged over the 28 answerable questions.

Dense ranks the direct answer better near the top. Hybrid finds more labelled evidence within five results, but sometimes pushes related passages above the answer. BM25 lowercases the text and splits on whitespace, so punctuation and math notation can get in the way of matching.

I tuned weights on these same questions, so I also built a held-out set (see below). The gold IDs list the passages I chose as evidence; other passages can also answer a question. Recall measures how much of that labelled evidence search finds. I check generated answers separately.

## Baseline answers

I checked the first 30-answer run against the current chunk texts, using the retrieved IDs:

- The model said it lacked evidence for both unanswerable questions.
- It also couldn't answer Q13. Search missed the definition of `[v]_B` and how reordering a basis changes coordinates.
- Every source ID mentioned in an answer was retrieved, but nine answers used plain IDs rather than the requested bracket citations.
- Q18 added an explanation absent from its evidence. Q29 needed to say that coordinate entries depend on an ordered basis.

The run saved IDs without passage snapshots, so I reviewed against the current corpus. I went through the answers one by one and didn't assign an accuracy score.

## LangGraph flow

`graph.py` runs the same retrieval and generation as a LangGraph graph, with two extra steps:

```text
retrieve -> check evidence -> answer
                 | not enough
                 v
           rewrite query (once) -> retrieve -> check evidence -> answer or abstain
```

The checker is a separate Qwen call. It reads the question and the five passages and returns JSON like `{"sufficient": false, "reason": "..."}`. If the evidence isn't enough, the rewriter turns the question into a search query using the checker's reason, and search runs again. After one rewrite the graph abstains instead of looping.

I ran it with the same 30 questions, corpus, model, and settings as the baseline:

| | Baseline | Graph |
| --- | ---: | ---: |
| Answerable questions answered | 27 / 28 | 28 / 28 |
| Unanswerable questions abstained | 2 / 2 | 2 / 2 |
| Recall@5 of the passages sent to the answer step | 91.7% | 95.2% |
| LLM calls for the 30 questions | 30 | 64 |
| Wall time for the 30 questions | 75 s | 124 s |
| Median seconds per question | 2.2 | 3.8 |

Three questions went through a rewrite:

- Q13 was the baseline's miss. The rewritten query put Definition 7.4 (`[v]_B` and basis reordering) at rank 1, and the answer matches that chunk.
- Q09 (eigenvalues) and Q30 (SVD) still had no evidence after the rewrite, so the graph abstained without calling the answer step.

The other 27 questions passed the check on the first try and got the same passages as the baseline.

Limits of this result:

- The gain is one question on the development set, and I built the rewrite step after seeing Q13 fail. The held-out check below shows it doesn't carry over cleanly.
- The evidence check adds about 1.5 s to every question, even the 27 that pass on the first try. The rewrite path adds about 3 s more. Times are from one run each on the GX10 with the model already loaded.
- The checker never rejected usable evidence on these questions. It did on the held-out set (H06).
- I haven't re-reviewed the other 27 regenerated answers line by line. Several answers still use bare IDs instead of bracket citations.

## Held-out check

After the graph and prompts were fixed, I added 16 new questions in [evaluation/heldout-eval-set.json](evaluation/heldout-eval-set.json): 13 answerable and three unanswerable. Most gold chunks are units that no dev question uses. H15 and H16 ask about kernels and rank-nullity, which are in Lectures 9 and 10 but outside the index. Nothing was tuned on these.

Retrieval on the 13 answerable questions:

| Retriever | Recall@1 | Recall@3 | Recall@5 |
| --- | ---: | ---: | ---: |
| Dense | 65.4% | 73.1% | 76.9% |
| BM25 | 38.5% | 73.1% | 73.1% |
| Hybrid, 75% dense weight | 57.7% | 73.1% | 76.9% |

Hybrid at five drops from 91.7% on the dev set to 76.9% here, and it's no better than dense alone. Part of the dev advantage came from tuning the weight on those questions.

Baseline vs. graph:

| | Baseline | Graph |
| --- | ---: | ---: |
| Answerable questions answered | 12 / 13 | 10 / 13 |
| Unanswerable questions abstained | 3 / 3 | 3 / 3 |
| Recall@5 of the passages sent to the answer step | 76.9% | 80.8% |
| Wall time for the 16 questions | 53 s | 58 s |

The graph helped once and hurt twice:

- H08 asks about `U_n(F)` and `D_n(F)`. The first search missed the upper triangular example (3.8), so the baseline answered half the question and guessed at the rest. The graph's rewrite spelled out "upper triangular" and "diagonal" and found both chunks.
- H06 asks whether `{0}` can be independent. Search missed Example 4.12, but the definition in 4.8 was enough to work it out, and the baseline did. The checker wanted the exact statement, so the graph abstained.
- H12 needs the short subspace test and the line-through-the-origin example. The baseline gave the test and said the example wasn't in its passages. The graph's rewrite still missed the example, so it abstained instead of giving the half it had.
- H10 failed in both. The question writes out the polynomials `{1-x-x^2, 2+3x+4x^2, 5-2x+x^2}`, and neither search found Example 7.10.

On new questions, the strict checker throws away answers the model could have built from related passages. On the dev set that never came up. Retrieval misses (H08, H10, H12) are the bigger problem, and the rewrite only fixes some of them.

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

`rag.py` answers all 30 questions and saves JSON with the answers, full retrieved passages, settings, and hashes of the corpus and dataset. The prompt asks for evidence-only answers and citations. Set `OLLAMA_URL` to override the default `http://127.0.0.1:11434/api/chat` endpoint.

To run the graph version on the same questions:

```sh
uv run python -m lecture_rag.graph
```

Both scripts take `--dataset evaluation/heldout-eval-set.json` and `--output` to run the held-out questions.

It saves answers, the checker's decision and reason, and the final passages to `artifacts/graph-answers.json`. The checker and rewriter call Ollama through `langchain-ollama`'s `ChatOllama`; the answer step reuses `generate_answer()` from `rag.py`. The answer step reads `OLLAMA_URL`; the checker and rewriter still use `ChatOllama`'s default local host.

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
- `graph.py`: LangGraph state, nodes, and routing for retrieve, check evidence, rewrite once, answer, or abstain.

The tests check corpus loading, eval wiring, and generation requests with mocked HTTP responses. Answer quality needs its own review. The converted corpus has 11 lectures and three practice files; the experiment indexes Lectures 1–7.

Each chunk keeps its original body and a `search_text` containing the lecture prefix, reviewed assumptions, and body. Lecture intros, trailing Source checks, practice files, and eval material stay out of the index. Source corrections and unresolved issues are recorded in each lecture's Source checks section.

## Next

Add a reranker over the top hybrid candidates, since early ranking and notation-heavy misses (H10) are the weakest part. Loosen the checker so it accepts answers that follow directly from the passages, and recheck H06. MRR and an answer-quality score are still pending.
