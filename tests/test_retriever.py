import numpy as np

from src.rag.retriever import Retriever


def test_retriever_return_most_relevant_chunk():
    chunks = [
        "Python is a programming language",
        "Banana is a fruit",
        "The sky is blue",
    ]

    embeddings = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.5, 0.5],
        ]
    )

    retriever = Retriever(embeddings, chunks)

    query_embedding = np.array([1.0, 0.0])
    results = retriever.retrieve(query_embedding, k=1)

    assert results == ["Python is a programming language"]
