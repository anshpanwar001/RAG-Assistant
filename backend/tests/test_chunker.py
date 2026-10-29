"""
Tests for the chunker.

Each test checks one behavior. Names describe what should happen, so a
failing test tells you what broke without reading the code.
"""

import pytest
from app.ingestion.chunker import chunk_document
from app.ingestion.loader import LoadedDocument


def test_neighboring_chunks_overlap_by_the_configured_amount():
    text = "".join(f"{i:04d}" for i in range(300))
    doc = LoadedDocument(source="numbers.txt", text=text)

    chunks = chunk_document(doc, chunk_size=50, chunk_overlap=10)

    # chunk 1 starts 40 characters in (50 minus the 10-character overlap)
    assert chunks[1].text[:10] == text[40:50]
    assert chunks[0].text[-10:] == chunks[1].text[:10]


def test_every_chunk_respects_the_maximum_size():
    text = "x" * 1000
    doc = LoadedDocument(source="long.txt", text=text)

    chunks = chunk_document(doc, chunk_size=120, chunk_overlap=20)

    assert all(len(chunk.text) <= 120 for chunk in chunks)


def test_empty_document_produces_no_chunks():
    doc = LoadedDocument(source="empty.txt", text="   \n  ")

    assert chunk_document(doc) == []


def test_chunks_keep_source_and_metadata():
    doc = LoadedDocument(source="handbook.pdf", text="hello " * 50, metadata={"page": 7})

    chunks = chunk_document(doc, chunk_size=100, chunk_overlap=10)

    assert all(chunk.source == "handbook.pdf" for chunk in chunks)
    assert all(chunk.metadata == {"page": 7} for chunk in chunks)


def test_overlap_not_smaller_than_size_is_rejected():
    doc = LoadedDocument(source="a.txt", text="some text")

    with pytest.raises(ValueError):
        chunk_document(doc, chunk_size=50, chunk_overlap=50)