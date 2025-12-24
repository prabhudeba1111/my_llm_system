import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))


class Retriever:
    def __init__(self, embeddings: np.ndarray, chunks: list[str]):
        self.embeddings = embeddings
        self.chunks = chunks

    def retrieve(self, query_embedding: np.ndarray, k: int = 3) -> list[str]:
        scores = [cosine_similarity(query_embedding, embedding) for embedding in self.embeddings]

        top_indices = sorted(range(len(scores)), 
                             key=lambda i: scores[i], 
                             reverse=True)[:k]
        
        return [self.chunks[i] for i in top_indices]