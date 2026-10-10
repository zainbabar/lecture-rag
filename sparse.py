from sentence_transformers import SentenceTransformer
import numpy as np
from prepare import prepare_experiment
import rank_bm25

def tokenize_chunks(chunks):
    texts = [chunk['search_text'] for chunk in chunks] # search texts
    texts = [text.lower() for text in texts] # full lowercase version of search text
    tokenized_texts = [text.split() for text in texts] # list lists, inner list is all words in a given chunks search text
    return tokenized_texts

def retrive(question, chunks, model, k=3):
    query_tokenized = question['question'].lower().split()
    scores = model.get_scores(query_tokenized)
    # we get 1 score per chunk in original order

    # indicies of our top k similar chunks to question
    top_k_indicies = np.flip(np.argsort(scores))[:k]

    top_k_chunk_ids = [chunks[i]['id'] for i in top_k_indicies]

    return top_k_chunk_ids

# measure recall@k (recall@3), what fraction of a questions gold chunks appeared in results
def recall_at_k(retrived_ids, gold_ids, k=3):
    appeared = [1 if id in gold_ids else 0 for id in retrived_ids[:k]]
    count = sum(appeared)
    recall = count / len(gold_ids)
    return recall


def main():
    recall5_scores = []
    recall3_scores = []
    recall1_scores = []
    eval_set, chunks = prepare_experiment()
    # turn each cunks search text into lowercase list of words
    tokenized_texts = tokenize_chunks(chunks)

    bm25 = rank_bm25.BM25Okapi(tokenized_texts) # build bm25 so it can calculate stats for search based on texts
    # stores stuff like how often each word appers in each chunk, how many chunks contain each word, each chunks length/avg len

    for question in eval_set['questions']:
        if question['score_retrieval'] == False: # if question has no gold id 
            continue
        retrived_ids = retrive(question, chunks, bm25, 5)
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
    

main()