import math

import pytest

from src.rag.chunker import chunk_text

text = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty"


def test_chunck_text_basic():
    words = text.split()
    total_words = len(words)
    chunk_size = 5
    overlap = 1
    step = chunk_size - overlap

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    for chunk in chunks:
        assert len(chunk.split()) <= chunk_size

    expected_chunks = math.ceil((total_words - chunk_size) / step) + 1
    assert len(chunks) == expected_chunks


def test_chunk_text_returns_strings():
    chunks = chunk_text(text)

    assert all(isinstance(c, str) for c in chunks)


def test_chunk_text_no_empty_chunks():
    chunks = chunk_text(text, chunk_size=50, overlap=10)

    assert all(chunk.strip() for chunk in chunks)


def test_chunk_size_less_than_overlap():
    with pytest.raises(ValueError, match="overlap"):
        chunk_text(text, chunk_size=10, overlap=10)
