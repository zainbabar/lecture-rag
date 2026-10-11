from rank_bm25 import BM25Okapi

from dense import embed_chunks, load_embedding_model, recall_at_k
from dense import retrive as dense_retrieve
from prepare import prepare_experiment
from sparse import retrive as sparse_retrieve
from sparse import tokenize_chunks


# combine dense + bm25 using ranks, since their raw scores aren't on the same scale
def hybrid_retrive(question, chunks, embeddings, dense_model, sparse_model, dense_weight, k):
    # get top 10 ids from both retrievers, then fuse down to the k we want
    dense_ranked_ids = dense_retrieve(question, chunks, embeddings, dense_model, 10)
    sparse_ranked_ids = sparse_retrieve(question, chunks, sparse_model, 10)

    # lower rank = earlier in that retriever's results, starting at 1
    scores = {}

    all_chunk_ids = list((set(dense_ranked_ids)) | (set(sparse_ranked_ids)))
    # a chunk can appear in either list or both; missing means no contribution
    for chunk_id in all_chunk_ids:
        dense_rank = dense_ranked_ids.index(chunk_id) + 1 if chunk_id in dense_ranked_ids else 0
        sprase_rank = sparse_ranked_ids.index(chunk_id) + 1 if chunk_id in sparse_ranked_ids else 0
        # 60 softens the gaps between ranks, so rank 1 doesn't dominate
        dense_score = 1 / (60 + dense_rank) if dense_rank != 0 else 0
        sparse_score = 1 / (60 + sprase_rank) if sprase_rank != 0 else 0

        # 0.75 gives dense more weight; 0.5 treats both lists equally
        hybrid_score = (dense_weight * dense_score) + (1 - dense_weight) * sparse_score
        scores[chunk_id] = hybrid_score

    # highest fused score first, then return just the top k ids
    sorted_scores = dict((sorted(scores.items(), key=lambda item: item[1], reverse=True)))
    top_k_chunks = list(sorted_scores.keys())[:k]
    return top_k_chunks


def main():
    # reuse the model + indexes across questions, not rebuild them per query
    dense_model = load_embedding_model()
    recall5_scores = []
    recall3_scores = []
    recall1_scores = []
    eval_set, chunks = prepare_experiment()
    # bm25 needs tokens; dense needs an embedding for each chunk
    tokenized_texts = tokenize_chunks(chunks)
    embeddings = embed_chunks(chunks, dense_model)
    sparse_model = BM25Okapi(tokenized_texts)

    for question in eval_set["questions"]:
        # unanswerable questions have no gold chunks, so skip recall for them
        if not question["score_retrieval"]:
            continue
        retrived_ids = hybrid_retrive(
            question, chunks, embeddings, dense_model, sparse_model, dense_weight=0.75, k=5
        )
        gold_ids = question["gold_chunk_ids"]
        recall5 = recall_at_k(retrived_ids, gold_ids, 5)
        recall3 = recall_at_k(retrived_ids, gold_ids, 3)
        recall1 = recall_at_k(retrived_ids, gold_ids, 1)
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
