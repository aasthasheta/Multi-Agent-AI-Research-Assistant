"""Embedding helpers used by the vector store."""
from __future__ import annotations
from app.utils.llm import embed_texts


def embed_chunks(texts: list[str], batch_size: int = 64) -> list[list[float]]:
    """Embed a list of texts in batches (keeps individual API calls small)."""
    vectors: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        vectors.extend(embed_texts(batch))
    return vectors
