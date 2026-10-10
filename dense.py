from sentence_transformers import SentenceTransformer
import numpy as np
from prepare import prepare_experiment

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5",
    device="mps",
    local_files_only=True,
)
texts = [
    "A basis is a linearly independent set that spans a vector space.",
    "The dimension of a vector space is the number of vectors in a basis.",
    "A subspace is closed under addition and scalar multiplication.",
]

embeddings = model.encode(texts)

question = "What makes a set of vectors a basis?"

query_embedding = model.encode( # bge recommended query instruction for embedding 
    "Represent this sentence for searching relevant passages: " + question
)

print(query_embedding.shape)


# have embedded our texts and our query, now see how similar they are 

# use cosine similarity to get similiarity scores between the question
# and each text embedding

# sim_scores = []
# q = query_embedding

# similarity indicies in ascending order of similarity, so lowest to highest
# sorted_indicies = np.argsort(sim_scores)

# for i in reversed(sorted_indicies):
#     print(f'text: {texts[i]}; similarity score: {sim_scores[i]}')
    
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

top_indices = rank_embeddings(query_embedding, embeddings, k=2)

for i in top_indices:
    print(i, texts[i])
        
        

   