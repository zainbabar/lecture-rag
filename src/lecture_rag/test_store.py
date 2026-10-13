from .dense import load_embedding_model
from .vector_store import BGEEmbeddings, retrieve
from .vector_store import load_store

# test that the retrival works from saved index -- WORKS!
def main():
    model = load_embedding_model()
    store = load_store(BGEEmbeddings(model=model))
    question = {"question": "What does it mean for vectors to be linearly independent?"}
    ids = retrieve(question=question, store=store)
    print(ids)
    
    
if __name__ == "__main__":
    main()