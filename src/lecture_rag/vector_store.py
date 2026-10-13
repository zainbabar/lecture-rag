from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from .dense import load_embedding_model
from .prepare import ROOT, prepare_experiment

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
   


def main() -> None:
    eval_set, chunks = prepare_experiment()  # only need the chunks for setup
    documents = chunks_to_documents(chunks=chunks)
    model = load_embedding_model()
    store = load_store(BGEEmbeddings(model=model))

    # now indexing aka adding documents to the chroma store
    # specificy the ids that we want documents to be stored with
    # databse id should be the same as the document/chunk id 
    ids = [doc.id for doc in documents]
    # langchain calls the embed_documents itself
    stored_ids = store.add_documents(documents=documents, ids=ids) # id goes thru **kwargs since not named param in add_documents
    # assert(ids == stored_ids) # make sure the stored ids are the same as the actual chunk ids 

    # question dict, test q 
    question = eval_set["questions"][0]
    ids = retrieve(question, store)
    print(ids)
    


if __name__ == "__main__":
    main()
