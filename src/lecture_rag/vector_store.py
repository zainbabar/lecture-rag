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
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # encode returns numpy arrays; langchain expects regular python lists
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        # same as dense.py: bge's search instruction goes on the query only
        return self.model.encode(QUERY_PREFIX + text).tolist()


# langchain uses Document objects instead of our chunk dicts
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


def load_store(embeddings: Embeddings, path: Path = STORE_PATH) -> Chroma:
    # reopen the saved collection, or create an empty one if this is the first run
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(path),
        # use cosine like our numpy retriever; chroma handles the search index
        collection_configuration={"hnsw": {"space": "cosine"}},
    )


def retrieve(question: dict, store: Chroma, k: int = 5) -> list[str]:
    pass


def main() -> None:
    _, chunks = prepare_experiment()  # only need the chunks for setup
    documents = chunks_to_documents(chunks)
    model = load_embedding_model()
    load_store(BGEEmbeddings(model))
    # todo: add the documents with their stable ids before trying retrieval
    print(f"Prepared {len(documents)} documents; store opened at {STORE_PATH}")
    print(f"Collection: {COLLECTION_NAME}. Indexing and retrieval are pending.")


if __name__ == "__main__":
    main()
