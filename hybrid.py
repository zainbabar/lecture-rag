from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from prepare import prepare_experiment
from dense import embed_chunks, recall_at_k
from dense import retrive as dense_retrieve
from sparse import tokenize_chunks
from sparse import retrive as sparse_retrieve

# aliases so we can tell the two search functions apart
# dense_retrieve(question, chunks, embeddings, model, k)
# sparse_retrieve(question, chunks, bm25, k)

# hybrid retrival with reciprocal rank fusion
def hybrid_retrive(question, chunks, embeddings, dense_model, sparse_model, dense_weight, k):
    # get top 10 ids from both retrivers for the same question
    dense_ranked_ids = dense_retrieve(question, chunks, embeddings, dense_model, 10)
    sparse_ranked_ids = sparse_retrieve(question, chunks, sparse_model, 10)
    
    # each chunk ids position/index above is its rank, so how similar each model thought it was
    scores = {} 

    all_chunk_ids = list((set(dense_ranked_ids)) | (set(sparse_ranked_ids)))
    for chunk_id in all_chunk_ids:
        dense_rank = dense_ranked_ids.index(chunk_id) + 1 if chunk_id in dense_ranked_ids else 0
        sprase_rank = sparse_ranked_ids.index(chunk_id) + 1 if chunk_id in sparse_ranked_ids else 0
        dense_score = 1 / (60 + dense_rank) if dense_rank != 0 else 0
        sparse_score = 1 / (60 + sprase_rank) if sprase_rank != 0 else 0
        
        hybrid_score = (dense_weight * dense_score) + (1 - dense_weight) * sparse_score
        scores[chunk_id] = hybrid_score
    
    
    # sort chunk score dict by the scores, use lambda and rebuild the dict w/ only top k
    sorted_scores = dict((sorted(scores.items(), key=lambda item: item[1], reverse=True)))
    top_k_chunks = list(sorted_scores.keys())[:k]
    return top_k_chunks


def main():
    dense_model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5",
        device="mps",
        local_files_only=True,
    )
    recall5_scores = []
    recall3_scores = []
    recall1_scores = []
    eval_set, chunks = prepare_experiment()
    # turn each cunks search text into lowercase list of words
    tokenized_texts = tokenize_chunks(chunks)
    embeddings = embed_chunks(chunks, dense_model)
    sparse_model = BM25Okapi(tokenized_texts)
    
    for question in eval_set['questions']:
        if question['score_retrieval'] == False:
            continue
        retrived_ids = hybrid_retrive(question, chunks, embeddings, dense_model, sparse_model, dense_weight=0.75, k=5)
        gold_ids = question['gold_chunk_ids']
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
