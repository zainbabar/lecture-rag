from .dense import load_embedding_model
from .vector_store import BGEEmbeddings, retrieve
from .vector_store import load_store
from .vector_store import get_passages
from .rag import generate_answer
import os


# try retrieval from the saved index, then generate an answer from the saved passages
def main():
    url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
    model = load_embedding_model()
    store = load_store(BGEEmbeddings(model=model))
    question = {"question": "What does it mean for vectors to be linearly independent?"}
    ids = retrieve(question=question, store=store)
    passages = get_passages(ids, store)
    answer = generate_answer(question, passages, url)
    print(answer)


if __name__ == "__main__":
    main()
