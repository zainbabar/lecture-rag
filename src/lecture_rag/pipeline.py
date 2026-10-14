from rank_bm25 import BM25Okapi

from .dense import load_embedding_model
from .prepare import DEFAULT_DATASET, prepare_experiment
from .rerank import load_rerank_model, rerank
from .sparse import retrieve as sparse_retrieve
from .sparse import tokenize_chunks
from .vector_store import BGEEmbeddings, load_store
from .vector_store import retrieve as chroma_retrieve


# use a class this time to make stuff cleaner vs more experimenty other files
# loads every model and index once, then answers questions with chroma + bm25 + rerank
class Pipeline:
    def __init__(self, dataset_path=DEFAULT_DATASET):
        # the store needs bge to embed questions, so it keeps its own reference
        embedding_model = load_embedding_model()
        self.store = load_store(BGEEmbeddings(model=embedding_model))
        # the index has to be built first, same as vector_store's --ask
        if not self.store.get()["ids"]:
            raise RuntimeError("the store is empty; run vector_store --index first")

        # bm25 and the reranker both read the chunk text, so keep the chunks too
        _, self.chunks = prepare_experiment(dataset_path)
        self.sparse_model = BM25Okapi(tokenize_chunks(self.chunks))
        self.rerank_model = load_rerank_model()

    # chroma top 10 + bm25 top 10, merged, then reranked down to k chunk ids
    def retrieve(self, question: dict, k: int = 5) -> list[str]:
        # get top 10 from chroma (dense) and sparse for reranking
        chroma_top_10 = chroma_retrieve(question, self.store, 10)
        bm25_top_10 = sparse_retrieve(question, self.chunks, self.sparse_model, k=10)
        candidate_ids = list(
            dict.fromkeys(chroma_top_10 + bm25_top_10)
        )  # merge in order & remove dups
        # feed candidates to rerank model to rerank and return top k ids
        top_k_ids = rerank(question, candidate_ids, self.chunks, self.rerank_model, k)
        return top_k_ids

    # chunk ids -> passages in the format generate_answer() expects
    def get_passages(self, ids: list[str]) -> list[dict]:
        passages = []
        # ids come back already ranked, so rank is just the position starting at 1
        for rank, chunk_id in enumerate(ids, start=1):
            for chunk in self.chunks:
                if chunk["id"] == chunk_id:
                    # search_text has the lecture prefix + checked assumptions + body
                    passages.append({"id": chunk_id, "passage": chunk["search_text"], "rank": rank})
                    break
        return passages
