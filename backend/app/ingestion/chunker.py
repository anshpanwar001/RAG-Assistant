"""
Split loaded documents into overlapping chunks.

Chunks are the unit we embed, store, and retrieve in later stages, so their
size strongly affects answer quality: too big and results are vague, too
small and the context is lost.
"""

from dataclasses import dataclass, field

from app.ingestion.loader import LoadedDocument


@dataclass
class Chunk:
    """A piece of a document, small enough to search and to fit in a prompt."""

    text: str
    source: str
    chunk_index: int  # position of this chunk within its source, starting at 0
    metadata: dict = field(default_factory=dict)


def chunk_document(
    document: LoadedDocument,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> list[Chunk]:
    """
    Split one document into chunks of at most `chunk_size` characters.

    Each new chunk starts `chunk_size - chunk_overlap` characters after the
    previous one, so neighboring chunks share `chunk_overlap` characters.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    text = document.text.strip()
    if not text:
        return []

    step = chunk_size - chunk_overlap
    chunks: list[Chunk] = []
    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            chunks.append(
                Chunk(
                    text=piece,
                    source=document.source,
                    chunk_index=index,
                    metadata=document.metadata,
                )
            )
            index += 1
        start += step

    return chunks


def chunk_documents(documents: list[LoadedDocument]) -> list[Chunk]:
    """Chunk a list of documents and return all chunks in one flat list."""
    all_chunks: list[Chunk] = []
    for document in documents:
        all_chunks.extend(chunk_document(document))
    return all_chunks