"""
Document ingestion: extract text from PDFs and split into overlapping chunks
ready for embedding.
"""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field

import fitz  # PyMuPDF

from app.utils.config import settings


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


def extract_text_from_pdf(path: str) -> str:
    """Extract raw text from every page of a PDF file."""
    text_parts = []
    with fitz.open(path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text")
            if text.strip():
                text_parts.append(text)
    return "\n".join(text_parts)


def chunk_text(text: str, source: str, chunk_size: int | None = None, overlap: int | None = None) -> list[Chunk]:
    """Split text into overlapping chunks by character count (simple, dependency-free)."""
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap or settings.chunk_overlap
    text = " ".join(text.split())  # normalize whitespace

    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        piece = text[start:end]
        chunks.append(
            Chunk(
                id=str(uuid.uuid4()),
                text=piece,
                metadata={"source": source, "start": start, "end": end},
            )
        )
        if end == n:
            break
        start = end - overlap  # step forward with overlap
    return chunks


def ingest_pdf(path: str, source_name: str | None = None) -> list[Chunk]:
    """Full ingestion pipeline for a single PDF: extract -> chunk."""
    source_name = source_name or path
    raw_text = extract_text_from_pdf(path)
    return chunk_text(raw_text, source=source_name)
