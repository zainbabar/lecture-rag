import os

import numpy as np
from sentence_transformers import SentenceTransformer

from .metrics import recall_at_k
from .prepare import ROOT, prepare_experiment

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
MODEL_CACHE = ROOT / ".cache" / "huggingface"


def load_embedding_model(device: str | None = None) -> SentenceTransformer:
    # None lets sentence transformers pick cuda, mps, or cpu
    # set LECTURE_RAG_DEVICE to override it without editing the scripts
    return SentenceTransformer(
        EMBEDDING_MODEL,
        device=device or os.environ.get("LECTURE_RAG_DEVICE"),
        cache_folder=str(MODEL_CACHE),
        local_files_only=True,
    )


def embed_chunks(chunks, model):
    # row i stays matched to chunks[i]; retrieval relies on that order
    texts = [chunk["search_text"] for chunk in chunks]  # prefix + assumptions + body
    text_embeddings = model.encode(texts)  # current corpus/model: (75, 384)
    return text_embeddings


# cosine similarity: compare vector direction, dividing out their lengths
def rank_embeddings(query_embedding, embeddings, k):
    similarity_scores = []
    q = query_embedding
    for v in embeddings:
        num = np.dot(q, v)
        denom = np.linalg.norm(q) * np.linalg.norm(v)
        similarity_score = num / denom
        similarity_scores.append(similarity_score)

    # argsort gives lowest first, flip it so the best matches come first
    # return indices so we can look up the chunks in the same order
    sorted_indices = np.flip(np.argsort(similarity_scores))

    top_k = sorted_indices[:k]

    return top_k


def retrieve(question, chunks, embeddings, model, k=3):
    query = question["question"]
    # bge's search instruction goes on the query, not the chunk texts
    bge_instruction = "Represent this sentence for searching relevant passages: "
    query_embedding = model.encode(bge_instruction + query)

    # get indices of the top k chunks for this query
    top_k_indices = rank_embeddings(query_embedding, embeddings, k)

    # turn row indices back into stable chunk ids, keeping the ranked order
    top_k_chunks = []

    for i in top_k_indices:
        top_k_chunks.append(chunks[i]["id"])

    return top_k_chunks


def main():
    model = load_embedding_model()

    eval_set, chunks = prepare_experiment()

    # embed the corpus once, then only embed each query during search
    embeddings = embed_chunks(chunks, model)

    k = 5

    recall5_scores = []
    recall3_scores = []
    recall1_scores = []

    for question in eval_set["questions"]:
        # recall needs gold ids, so leave unanswerable questions out
        if not question["score_retrieval"]:
            continue
        retrieved_ids = retrieve(question, chunks, embeddings, model, k)
        gold_ids = question["gold_chunk_ids"]
        recall5 = recall_at_k(retrieved_ids, gold_ids, 5)
        recall3 = recall_at_k(retrieved_ids, gold_ids, 3)
        recall1 = recall_at_k(retrieved_ids, gold_ids, 1)
        recall5_scores.append(recall5)
        recall3_scores.append(recall3)
        recall1_scores.append(recall1)
        # to inspect misses, compare retrieved_ids with gold_ids here

    # average per-question recall, so each scored question has equal weight
    avg_recall_at_5 = sum(recall5_scores) / len(recall5_scores)
    avg_recall_at_3 = sum(recall3_scores) / len(recall3_scores)
    avg_recall_at_1 = sum(recall1_scores) / len(recall1_scores)

    print(f"average recall@5: {avg_recall_at_5}")
    print(f"average recall@3: {avg_recall_at_3}")
    print(f"average recall@1: {avg_recall_at_1}")


if __name__ == "__main__":
    main()
