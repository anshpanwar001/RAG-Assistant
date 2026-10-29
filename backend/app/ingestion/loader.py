"""
Load documents from disk and return their text.

Each document becomes a LoadedDocument: the extracted text plus metadata
that we keep so answers can later cite where the text came from.
"""

from dataclasses import dataclass, field
from pathlib import Path

from pypdf import PdfReader


class UnsupportedFileTypeError(Exception):
    """Raised when a file extension is not one we know how to read."""


@dataclass
class LoadedDocument:
    """A file's full text, plus metadata that travels with every chunk later."""

    source: str  # the file name, shown to users as the citation
    text: str
    metadata: dict = field(default_factory=dict)


def _load_pdf(path: Path) -> list[LoadedDocument]:
    """Extract text one page at a time, so each page keeps its page number."""
    reader = PdfReader(str(path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():  # skip blank pages, such as image-only scans
            pages.append(
                LoadedDocument(
                    source=path.name,
                    text=text,
                    metadata={"page": page_number},
                )
            )
    return pages

def load_directory(folder: Path) -> list[LoadedDocument]:
    """
    Load every supported file in a folder, in alphabetical order.

    Files with unsupported extensions and hidden files (names starting
    with a dot, such as .DS_Store on macOS) are skipped.
    """
    if not folder.is_dir():
        raise NotADirectoryError(f"'{folder}' is not a folder")

    documents: list[LoadedDocument] = []
    for path in sorted(folder.iterdir()):
        if path.name.startswith("."):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in LOADERS:
            continue
        documents.extend(load_document(path))
    return documents


def _load_text(path: Path) -> list[LoadedDocument]:
    """Read a plain text or Markdown file as one document."""
    text = path.read_text(encoding="utf-8")
    return [LoadedDocument(source=path.name, text=text)]


LOADERS = {
    ".pdf": _load_pdf,
    ".txt": _load_text,
    ".md": _load_text,
}


def load_document(path: Path) -> list[LoadedDocument]:
    """
    Load a file and return one or more LoadedDocument objects.

    A PDF returns one document per non-empty page. A text file returns one document.
    """
    loader = LOADERS.get(path.suffix.lower())
    if loader is None:
        supported = ", ".join(LOADERS)
        raise UnsupportedFileTypeError(
            f"'{path.suffix}' is not supported. Supported types: {supported}"
        )
    return loader(path)