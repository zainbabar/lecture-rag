import argparse

from .graph import build_graph
from .prepare import DEFAULT_DATASET
from .rag import load_retriever


# ask one question: chroma + bm25 + rerank, then the graph checks the evidence and answers
def main() -> None:
    parser = argparse.ArgumentParser(description="Ask a question about the MATH 235 notes.")
    parser.add_argument("question", type=str)
    args = parser.parse_args()

    # the dataset is only used to pick which lecture files to load
    _, retrieve_passages = load_retriever("rerank", DEFAULT_DATASET)
    graph = build_graph(retrieve_passages)
    result = graph.invoke(
        {
            "question": args.question,
            "retrieval_query": args.question,
            "rewrite_count": 0,
            "path": [],
        }
    )

    print(result["answer"])
    print()
    print("passages:", [passage["id"] for passage in result["passages"]])
    print("path:", " -> ".join(result["path"]))


if __name__ == "__main__":
    main()
