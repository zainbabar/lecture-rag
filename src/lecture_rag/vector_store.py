import argparse
import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from sentence_transformers import SentenceTransformer

from .dense import load_embedding_model
from .metrics import mrr, recall_at_k
from .prepare import DEFAULT_DATASET, ROOT, prepare_experiment
from .rag import generate_answer

# save the index locally; .cache is already gitignored
STORE_PATH = ROOT / ".cache" / "chroma"
COLLECTION_NAME = "math235"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")


# langchain expects these two methods, so wrap the bge model we already use
class BGEEmbeddings(Embeddings):
    def __init__(self, model: SentenceTransformer) -> None:
        self.model = model  # keeps ref to model we already loaded

    # langchain pulls out each document's page_content and passes those strings here
    # this func builds the vectors; chroma saves them and updates the index after
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # encode returns numpy arrays; langchain expects regular python lists
        return self.model.encode(texts).tolist()

    # embed question
    def embed_query(self, text: str) -> list[float]:
        # same as dense.py: bge's search instruction goes on the query only
        return self.model.encode(QUERY_PREFIX + text).tolist()


# langchain uses Document objects instead of our chunk dicts
# turn our chunk dicts into Documents for langchain's add_documents call
def chunks_to_documents(chunks: list[dict]) -> list[Document]:
    return [
        Document(
            id=chunk["id"],
            page_content=chunk["search_text"],
            metadata={
                "id": chunk["id"],  # extra copy in metadata; retrieve uses doc.id
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


# open the saved chroma database so we can add documents or search
def load_store(embeddings: Embeddings, path: Path = STORE_PATH) -> Chroma:
    # reopen the saved collection, or create an empty one if this is the first run
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(path),
        # use cosine like our numpy retriever; chroma handles the search index
        collection_configuration={"hnsw": {"space": "cosine"}},
    )


# take a question dict and return ranked chunk ids like our other retrievers
def retrieve(question: dict, store: Chroma, k: int = 5) -> list[str]:
    # make the retriever; k sets how many results to ask for when we invoke it
    retriever = store.as_retriever(search_kwargs={"k": k})
    # .invoke() uses (cosine) similarity search
    # uses the chroma search not our hybrid thing
    retrieved_documents = retriever.invoke(
        question["question"]
    )  # returns up to k Documents in similarity order

    # want to get just the ids not the whole document IN ORDER
    ids = [doc.id for doc in retrieved_documents]
    return ids


# take the retrieved ids and return formatted passages for generate_answer()
def get_passages(retrieved_ids: list[str], store: Chroma) -> list[dict]:
    documents = store.get(
        retrieved_ids
    )  # parallel lists of ids, text, metadata; same index = same record
    passages = []
    # get() doesn't promise retrieval order, so follow our ranked ids
    for rank, chunk_id in enumerate(retrieved_ids, start=1):
        idx = documents["ids"].index(chunk_id)  # match the id with its saved text
        passage = documents["documents"][idx]  # saved page_content strings, not Document objects
        passages.append({"id": chunk_id, "passage": passage, "rank": rank})

    return passages


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Index the notes, evaluate retrieval, or ask a question."
    )
    # pick one mode; don't re-embed the chunks when we just want to evaluate
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--index", action="store_true", help="embed and save the chunks")
    modes.add_argument(
        "--evaluate", action="store_true", help="score retrieval from the saved index"
    )
    modes.add_argument("--ask", type=str, help="answer a question using the saved passages")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()

    model = load_embedding_model()
    store = load_store(BGEEmbeddings(model=model))

    if args.index:
        _, chunks = prepare_experiment(args.dataset)
        documents = chunks_to_documents(chunks=chunks)
        ids = [doc.id for doc in documents]
        # langchain embeds the text, then chroma saves it under our chunk ids
        # ids goes through **kwargs since it isn't a named parameter in add_documents
        stored_ids = store.add_documents(documents=documents, ids=ids)
        print(f"Saved {len(stored_ids)} chunks to {STORE_PATH}")
        return

    # asking and evaluating both need a saved index
    if not store.get()["ids"]:
        parser.error("the store is empty; run --index first")

    if args.ask is not None:
        question = {"question": args.ask}
        ids = retrieve(question=question, store=store)
        passages = get_passages(ids, store)
        answer = generate_answer(question, passages, URL)
        print(answer)
        return

    # same recall calculation as dense.py; only the retrieval call changes
    eval_set, _ = prepare_experiment(args.dataset)
    recall1_scores = []
    recall3_scores = []
    recall5_scores = []
    all_retrieved_ids = []
    all_gold_ids = []
    for question in eval_set["questions"]:
        if not question["score_retrieval"]:
            continue  # no gold ids means no recall score
        retrieved_ids = retrieve(question, store, k=5)
        gold_ids = question["gold_chunk_ids"]
        all_retrieved_ids.append(retrieved_ids)
        all_gold_ids.append(gold_ids)
        recall1_scores.append(recall_at_k(retrieved_ids, gold_ids, 1))
        recall3_scores.append(recall_at_k(retrieved_ids, gold_ids, 3))
        recall5_scores.append(recall_at_k(retrieved_ids, gold_ids, 5))

    if not recall1_scores:
        parser.error("this dataset has no questions scored for retrieval")
    print(f"Dataset: {args.dataset}; scored {len(recall1_scores)} questions")
    print(f"average recall@1: {sum(recall1_scores) / len(recall1_scores)}")
    print(f"average recall@3: {sum(recall3_scores) / len(recall3_scores)}")
    print(f"average recall@5: {sum(recall5_scores) / len(recall5_scores)}")
    print(f"MRR@5: {mrr(all_retrieved_ids, all_gold_ids, k=5)}")


if __name__ == "__main__":
    main()
