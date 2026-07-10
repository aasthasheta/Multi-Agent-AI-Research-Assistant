"""
RAG Agent
---------
Reads previously-ingested PDF documents (via the vector store) and retrieves
the chunks most relevant to the current query/objectives.
"""
from __future__ import annotations
from app.rag.retriever import retrieve_context, format_context_block


def get_document_context(query: str, top_k: int = 5) -> tuple[list[dict], str]:
    hits = retrieve_context(query, top_k=top_k)
    return hits, format_context_block(hits)
