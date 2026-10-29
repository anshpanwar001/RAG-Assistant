"""
The ingestion pipeline: from a folder of files to a list of chunks.

Later stages will add embedding and storage here. Callers only need to
know this one function, so the steps can change without touching them.
"""

from pathlib import Path

from app.ingestion.chunker import Chunk, chunk_documents
from app.ingestion.loader import load_directory


def ingest_folder(folder: Path) -> list[Chunk]:
    """Load every supported file in `folder` and return all of their chunks."""
    documents = load_directory(folder)
    chunks = chunk_documents(documents)
    return chunks