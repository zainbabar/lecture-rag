import argparse
import os
import time
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from .dense import MODEL_CACHE, embed_chunks, load_embedding_model
from .dense import retrieve as dense_retrieve
from .metrics import mrr, recall_at_k
from .prepare import DEFAULT_DATASET, prepare_experiment
from .sparse import retrieve as sparse_retrieve
from .sparse import tokenize_chunks


RERANK_MODEL = "BAAI/bge-reranker-base"


def load_rerank_model(device: str | None = None) -> CrossEncoder:
    # same device override as the embedding model
    # no local_files_only here so the first run can download the weights
    return CrossEncoder(
        RERANK_MODEL,
        device=device or os.environ.get("LECTURE_RAG_DEVICE"),
        cache_folder=str(MODEL_CACHE),
    )
    
# take top candidates ids and chunks, rerank the chunksbased on relevance score with the question
# return the top k ids ordered by relevance
def rerank(question: dict, candidate_ids: list, chunks: list[dict], rerank_model: CrossEncoder, k=5) -> list:
    # need the actual passage text of the candidate chunks to get a relevance score
    # but keep it in order so we can match up candidate id with its text
    candidate_texts = []
    for id in candidate_ids:
        for chunk in chunks:
            if chunk["id"] == id:
                candidate_texts.append(chunk["search_text"])
                break # break out if found no point continuing
    # now indexes match, id at candidate_ids[0]'s search text is candidate_texts[0]

    pairs = [[question["question"], passage] for passage in candidate_texts] # input pairs
    scores = rerank_model.predict(pairs)
    
    # need to sort the indicies by the value they point to
    # instead of value themselves
    # so we dont lose the index correspondance 
    sorted_indicies = np.argsort(scores, descending=True) # best first
    top_k_indicies = sorted_indicies[:k]

    top_k_ids = [candidate_ids[i] for i in top_k_indicies]
    return top_k_ids
         


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()

    # load every model once, not per question
    dense_model = load_embedding_model()
    rerank_model = load_rerank_model()
    eval_set, chunks = prepare_experiment(args.dataset)
    tokenized_texts = tokenize_chunks(chunks)
    embeddings = embed_chunks(chunks, dense_model)
    sparse_model = BM25Okapi(tokenized_texts)

    recall5_scores = []
    recall3_scores = []
    recall1_scores = []
    all_retrieved_ids = []
    all_gold_ids = []
    rerank_seconds = []

    for question in eval_set["questions"]:
        # unanswerable questions have no gold chunks, so skip them
        if not question["score_retrieval"]:
            continue

        # candidates are the top 10 from each retriever, merged with no duplicates
        dense_ids = dense_retrieve(question, chunks, embeddings, dense_model, 10)
        sparse_ids = sparse_retrieve(question, chunks, sparse_model, 10)
        candidate_ids = list(dict.fromkeys(dense_ids + sparse_ids)) # remove duplicates and keep the order

        # time only the reranking step, that's the latency it adds
        start = time.perf_counter()
        retrieved_ids = rerank(question, candidate_ids, chunks, rerank_model, 5)
        rerank_seconds.append(time.perf_counter() - start)

        gold_ids = question["gold_chunk_ids"]
        all_retrieved_ids.append(retrieved_ids)
        all_gold_ids.append(gold_ids)
        recall5_scores.append(recall_at_k(retrieved_ids, gold_ids, 5))
        recall3_scores.append(recall_at_k(retrieved_ids, gold_ids, 3))
        recall1_scores.append(recall_at_k(retrieved_ids, gold_ids, 1))

    avg_recall_at_5 = sum(recall5_scores) / len(recall5_scores)
    avg_recall_at_3 = sum(recall3_scores) / len(recall3_scores)
    avg_recall_at_1 = sum(recall1_scores) / len(recall1_scores)

    print(f"average recall@5: {avg_recall_at_5}")
    print(f"average recall@3: {avg_recall_at_3}")
    print(f"average recall@1: {avg_recall_at_1}")
    print(f"MRR@5: {mrr(all_retrieved_ids, all_gold_ids, k=5)}")
    print(f"average rerank seconds per question: {sum(rerank_seconds) / len(rerank_seconds)}")


if __name__ == "__main__":
    main()
