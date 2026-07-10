"""High-level retrieval helper used by the RAG Agent."""
from __future__ import annotations
from app.rag.vector_store import get_vector_store


def retrieve_context(query: str, top_k: int = 5) -> list[dict]:
    """Return the top-k most relevant chunks for a query, or [] if the store is empty."""
    store = get_vector_store()
    if store.document_count() == 0:
        return []
    return store.query(query, top_k=top_k)


def format_context_block(hits: list[dict]) -> str:
    """Turn retrieved chunks into a numbered context block for prompting."""
    if not hits:
        return "No relevant uploaded documents were found."
    lines = []
    for i, hit in enumerate(hits, start=1):
        source = hit["metadata"].get("source", "unknown")
        lines.append(f"[{i}] (source: {source})\n{hit['text']}")
    return "\n\n".join(lines)
