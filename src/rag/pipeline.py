from src.rag.chunker import chunk_text
from src.rag.embedder import Embedder
from src.rag.loader import load_text_documents
from src.rag.retriever import Retriever


class RAGPipeline:
    def __init__(self, docs_path: str):
        documents = load_text_documents(docs_path)

        chunks = []
        for doc in documents:
            chunks.extend(chunk_text(doc))

        self.chunks = chunks
        self.embedder = Embedder()
        self.chunk_embeddings = self.embedder.embed(chunks)
        self.retriever = Retriever(self.chunk_embeddings, chunks)

    def retrieve(self, query: str, k: int = 3):
        query_embeddings = self.embedder.embed([query])[0]
        return self.retriever.retrieve(query_embeddings, k)
