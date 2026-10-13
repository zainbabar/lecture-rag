import numpy as np
import rank_bm25

from .metrics import recall_at_k
from .prepare import prepare_experiment


def tokenize_chunks(chunks):
    # keep punctuation/math symbols as-is for this baseline; split on whitespace
    texts = [chunk["search_text"] for chunk in chunks]  # search texts
    texts = [text.lower() for text in texts]  # full lowercase version of search text
    tokenized_texts = [text.split() for text in texts]  # one token list per chunk
    return tokenized_texts


def retrieve(question, chunks, model, k=3):
    # query and corpus need the same tokenization for word matches to work
    query_tokenized = question["question"].lower().split()
    scores = model.get_scores(query_tokenized)
    # we get 1 score per chunk in original order

    # argsort is lowest first, so flip it to get the highest bm25 scores
    top_k_indices = np.flip(np.argsort(scores))[:k]

    top_k_chunk_ids = [chunks[i]["id"] for i in top_k_indices]

    return top_k_chunk_ids


def main():
    recall5_scores = []
    recall3_scores = []
    recall1_scores = []
    eval_set, chunks = prepare_experiment()
    # build the corpus stats once, then reuse bm25 for every question
    tokenized_texts = tokenize_chunks(chunks)

    bm25 = rank_bm25.BM25Okapi(tokenized_texts)
    # tracks word counts, how many chunks contain each word, and chunk lengths

    for question in eval_set["questions"]:
        if not question["score_retrieval"]:  # no gold ids means no recall score
            continue
        retrieved_ids = retrieve(question, chunks, bm25, 5)
        gold_ids = question["gold_chunk_ids"]
        recall5 = recall_at_k(retrieved_ids, gold_ids, 5)
        recall3 = recall_at_k(retrieved_ids, gold_ids, 3)
        recall1 = recall_at_k(retrieved_ids, gold_ids, 1)
        recall5_scores.append(recall5)
        recall3_scores.append(recall3)
        recall1_scores.append(recall1)

    avg_recall_at_5 = sum(recall5_scores) / len(recall5_scores)
    avg_recall_at_3 = sum(recall3_scores) / len(recall3_scores)
    avg_recall_at_1 = sum(recall1_scores) / len(recall1_scores)

    print(f"average recall@5: {avg_recall_at_5}")
    print(f"average recall@3: {avg_recall_at_3}")
    print(f"average recall@1: {avg_recall_at_1}")


if __name__ == "__main__":
    main()
