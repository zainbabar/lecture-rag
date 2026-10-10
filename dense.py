from sentence_transformers import SentenceTransformer
import numpy as np
from prepare import prepare_experiment


# prepare_experiment() returns eval set w/ questions and gold labels (specific / best chunk we want)
# and chunks, the prepared and chunked lecture passages 

# chunks = list of dicts, one per lecture unit
#   id: stable name like 'lecture-03-unit-3.7'
#   search_text: the text we embed (prefix + assumptions + body)
#   text: original body
#   lecture, type, section, title: what this unit is
#   source_file, pages: where it came from
#   context_prefix, lecture_intro, assumptions: extra context

# eval_set = dict describing the retrieval experiment
#   corpus['files']: which lecture files we're searching
#   questions: list of question dicts
#     id, question: question identifier and actual question
#     answerable: whether the corpus has enough evidence
#     gold_chunk_ids: chunks we want search to find
#     supporting_chunk_ids: useful extras, don't count as gold
#     score_retrieval: whether to include it in retrieval metrics

# load the eval set and chunks

def embed_chunks(chunks, model):
    texts = [chunk['search_text'] for chunk in chunks] # collect the chunks search text (what we want to embed)
    text_embeddings = model.encode(texts) # matrix of embeddings of all our chunks, 75 vectors -> shape is (75, 384)
    return text_embeddings

# scoring and sorting function. returns top k similar texts indicies 
def rank_embeddings(query_embedding, embeddings, k):
    similarity_scores = []
    q = query_embedding
    for v in embeddings:
        num = np.dot(q, v)
        denom = np.linalg.norm(q) * np.linalg.norm(v)
        similarity_score = num / denom
        similarity_scores.append(similarity_score)
    
    # return the indicies of highest to lowest similarity score
    # indicies so we can match up with the original text, since they correspond
    sorted_indicies = np.flip(np.argsort(similarity_scores))

    top_k = sorted_indicies[:k]

    return top_k

def retrive(question, chunks, embeddings, model, k=3):
    bge_instruction = "Represent this sentence for searching relevant passages: "
    query_embedding = model.encode(bge_instruction + question)

    # get top k similar text indicies to query
    top_k_indicies = rank_embeddings(query_embedding, embeddings, k)
    
    # ids of the top k chunks corresponding to indicies in ranked order
    top_k_chunks = []

    for i in top_k_indicies:
        top_k_chunks.append(chunks[i]['id'])
        
    return top_k_chunks

# measure recall@k (recall@3), what fraction of a questions gold chunks appeared in results
def recall_at_k(retrived_ids, gold_ids, k=3):
    appeared = [1 if id in gold_ids else 0 for id in retrived_ids[:k]]
    count = sum(appeared)
    recall = count / len(gold_ids)
    return recall



def main():
    model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5",
        device="mps",
        local_files_only=True,
    )

    eval_set, chunks = prepare_experiment()

    question = "what makes a set of vectors a basis?"

    embeddings = embed_chunks(chunks, model)

    k = 5

    recall5_scores = []
    recall3_scores = []
    recall1_scores = []

    for question in eval_set['questions']:
        if question['score_retrieval'] == False:
            continue
        q = question['question'] # the acutal question text
        retrived_ids = retrive(q, chunks, embeddings, model, k)
        gold_ids = question['gold_chunk_ids']
        recall5 = recall_at_k(retrived_ids, gold_ids, 5)
        recall3 = recall_at_k(retrived_ids, gold_ids, 3)
        recall1 = recall_at_k(retrived_ids, gold_ids, 1)
        recall5_scores.append(recall5)
        recall3_scores.append(recall3)
        recall1_scores.append(recall1)
        # inspect misses
        # print(f'{q}, top 3 retrived ids: {top_k_match_ids}, gold chunk ids: {question['gold_chunk_ids']}')

    avg_recall_at_5 = sum(recall5_scores) / len(recall5_scores)
    avg_recall_at_3 = sum(recall3_scores) / len(recall3_scores)
    avg_recall_at_1 = sum(recall1_scores) / len(recall1_scores)

    print(f"average recall@5: {avg_recall_at_5}")
    print(f"average recall@3: {avg_recall_at_3}")
    print(f"average recall@1: {avg_recall_at_1}")
    

main()