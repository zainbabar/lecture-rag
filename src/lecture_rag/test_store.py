from .dense import load_embedding_model
from .vector_store import BGEEmbeddings, retrieve
from .vector_store import load_store
from .vector_store import get_passages
from .vector_store import chunks_to_documents
from .prepare import prepare_experiment
from .rag import generate_answer
import os

# test that the retrival works from saved index -- WORKS!
def main():
    url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
    _, chunks = prepare_experiment()
    model = load_embedding_model()
    store = load_store(BGEEmbeddings(model=model))
    question = {"question": "What does it mean for vectors to be linearly independent?"}
    ids = retrieve(question=question, store=store)
    documents = chunks_to_documents(chunks)
    passages = get_passages(ids, documents)
    answer = generate_answer(question, passages, url)
    print(answer)

    
    
if __name__ == "__main__":
    main()