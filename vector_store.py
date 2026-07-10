"""
Persistent ChromaDB vector store wrapper.

Stores document chunks with their embeddings and metadata so the RAG Agent
can perform semantic search across everything the user has uploaded.
"""
from __future__ import annotations
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.utils.config import settings
from app.rag.ingest import Chunk
from app.rag.embeddings import embed_chunks

COLLECTION_NAME = "research_documents"


class VectorStore:
    def __init__(self, persist_dir: str | None = None):
        self.client = chromadb.PersistentClient(
            path=persist_dir or settings.chroma_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def add_chunks(self, chunks: list[Chunk]) -> int:
        if not chunks:
            return 0
        texts = [c.text for c in chunks]
        vectors = embed_chunks(texts)
        self.collection.add(
            ids=[c.id for c in chunks],
            embeddings=vectors,
            documents=texts,
            metadatas=[c.metadata for c in chunks],
        )
        return len(chunks)

    def query(self, query_text: str, top_k: int = 5) -> list[dict]:
        from app.utils.llm import embed_texts

        query_vector = embed_texts([query_text])[0]
        results = self.collection.query(query_embeddings=[query_vector], n_results=top_k)

        hits = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for doc, meta, dist in zip(docs, metas, dists):
            hits.append({"text": doc, "metadata": meta, "distance": dist})
        return hits

    def document_count(self) -> int:
        return self.collection.count()


_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    """Singleton accessor so the whole app shares one Chroma connection."""
    global _store
    if _store is None:
        _store = VectorStore()
    return _store
