import argparse
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from .dense import load_embedding_model
from .metrics import recall_at_k
from .prepare import DEFAULT_DATASET, ROOT, prepare_experiment

# save the index locally; .cache is already gitignored
STORE_PATH = ROOT / ".cache" / "chroma"
COLLECTION_NAME = "math235"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# langchain expects these two methods, so wrap the bge model we already use
class BGEEmbeddings(Embeddings):
    def __init__(self, model: SentenceTransformer) -> None:
        self.model = model # keeps ref to model we already loaded

    # texts is the page_content fields in doucments, langchain gets this and gives it to function
    # this func builds the vector, chroma builds index after
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # encode returns numpy arrays; langchain expects regular python lists
        return self.model.encode(texts).tolist()

    # embed question 
    def embed_query(self, text: str) -> list[float]:
        # same as dense.py: bge's search instruction goes on the query only
        return self.model.encode(QUERY_PREFIX + text).tolist()


# langchain uses Document objects instead of our chunk dicts
# after we chunk the md, we need to turn it into Document for langchain stuff to work
def chunks_to_documents(chunks: list[dict]) -> list[Document]:
    return [
        Document(
            id=chunk["id"],
            page_content=chunk["search_text"],
            metadata={
                "id": chunk["id"],  # keep the id here too so retrieval can return it
                "lecture": chunk["lecture"],
                "section": chunk["section"],
                "type": chunk["type"],
                # store pages as a string so we don't depend on list metadata support
                "pages": ", ".join(str(page) for page in chunk["pages"]),
                "source_file": chunk["source_file"],
            },
        )
        for chunk in chunks
    ]


# open chroma database on disk and give us the acutal object we can use 
def load_store(embeddings: Embeddings, path: Path = STORE_PATH) -> Chroma:
    # reopen the saved collection, or create an empty one if this is the first run
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(path),
        # use cosine like our numpy retriever; chroma handles the search index
        collection_configuration={"hnsw": {"space": "cosine"}},
    )

# take question dict and return ranked chunk ids like our current hybrid/dense/sparse retrivers
def retrieve(question: dict, store: Chroma, k: int = 5) -> list[str]:
    # build langchain retriver from our chroma store, return k results 
    retriver = store.as_retriever(search_kwargs={"k": k})
    # .invoke() uses (cosine) similarity search
    # uses the chroma search not our hybrid thing
    retrived_documents = retriver.invoke(question["question"]) # returns ordered top k matching Documents 

    # want to get just the ids not the whole document IN ORDER
    ids = [doc.id for doc in retrived_documents]
    return ids

# take the retrieved ids and return formatted passages for generate_answer()
def get_passages(retrieved_ids: list[str], documents: list[Document]):
    passages = []
    # for each rank id pair in retrived ids, get matching document 
    for rank, id in enumerate(retrieved_ids, start=1):
        for doc in documents:
            if doc.id == id:
                passages.append({"id": id, "passage": doc.page_content, "rank": rank})
                break # break out no reason to keep searching after
    
    return passages
        
    

   


def main() -> None:
    parser = argparse.ArgumentParser(description="Index the notes or evaluate Chroma retrieval.")
    # pick one mode; don't re-embed the chunks when we just want to evaluate
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--index", action="store_true", help="embed and save the chunks")
    modes.add_argument("--evaluate", action="store_true", help="score retrieval from the saved index")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()

    eval_set, chunks = prepare_experiment(args.dataset)
    model = load_embedding_model()
    store = load_store(BGEEmbeddings(model=model))

    if args.index:
        documents = chunks_to_documents(chunks=chunks)
        ids = [doc.id for doc in documents]
        # langchain embeds the text, then chroma saves it under our chunk ids
        # ids goes through **kwargs since it isn't a named parameter in add_documents
        stored_ids = store.add_documents(documents=documents, ids=ids)
        print(f"Saved {len(stored_ids)} chunks to {STORE_PATH}")
        return

    # don't report zero recall just because we forgot to index
    if not store.get()["ids"]:
        parser.error("the store is empty; run --index first")

    # same recall calculation as dense.py; only the retrieval call changes
    recall1_scores = []
    recall3_scores = []
    recall5_scores = []
    for question in eval_set["questions"]:
        if not question["score_retrieval"]:
            continue  # no gold ids means no recall score
        retrieved_ids = retrieve(question, store, k=5)
        gold_ids = question["gold_chunk_ids"]
        recall1_scores.append(recall_at_k(retrieved_ids, gold_ids, 1))
        recall3_scores.append(recall_at_k(retrieved_ids, gold_ids, 3))
        recall5_scores.append(recall_at_k(retrieved_ids, gold_ids, 5))

    if not recall1_scores:
        parser.error("this dataset has no questions scored for retrieval")
    print(f"Dataset: {args.dataset}; scored {len(recall1_scores)} questions")
    print(f"average recall@1: {sum(recall1_scores) / len(recall1_scores)}")
    print(f"average recall@3: {sum(recall3_scores) / len(recall3_scores)}")
    print(f"average recall@5: {sum(recall5_scores) / len(recall5_scores)}")


if __name__ == "__main__":
    main()
