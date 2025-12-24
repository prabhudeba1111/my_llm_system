from src.rag.pipeline import RAGPipeline


def test_rag_pipeline_retrieve_context(tmp_path):
    doc = tmp_path / "doc.txt"
    doc.write_text(
        "Python is great for backend systems.\n"
        "Java is also popular.\n"
    )

    rag = RAGPipeline(docs_path=str(tmp_path))
    context = rag.retrieve("Python")

    assert any("Python" in c for c in context)