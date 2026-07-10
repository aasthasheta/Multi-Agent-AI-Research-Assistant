"""
Memory Agent
------------
Stores previous conversations/research runs in SQLite so the system can
support follow-up questions and maintain research history across sessions.
"""
from __future__ import annotations
import sqlite3
import time
import json
from contextlib import contextmanager

from app.utils.config import settings

_SCHEMA = """
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,           -- 'user' or 'assistant'
    content TEXT NOT NULL,
    metadata TEXT,
    created_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_history_session ON history(session_id);
"""


@contextmanager
def _connect():
    conn = sqlite3.connect(settings.memory_db_path)
    try:
        conn.executescript(_SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def add_message(session_id: str, role: str, content: str, metadata: dict | None = None) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO history (session_id, role, content, metadata, created_at) VALUES (?, ?, ?, ?, ?)",
            (session_id, role, content, json.dumps(metadata or {}), time.time()),
        )


def get_history(session_id: str, limit: int = 20) -> list[dict]:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT role, content, metadata, created_at FROM history "
            "WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        )
        rows = cur.fetchall()
    rows.reverse()
    return [
        {"role": r[0], "content": r[1], "metadata": json.loads(r[2] or "{}"), "created_at": r[3]}
        for r in rows
    ]


def format_history_block(session_id: str, limit: int = 10) -> str:
    history = get_history(session_id, limit=limit)
    if not history:
        return "No prior conversation history."
    lines = [f"{h['role'].upper()}: {h['content']}" for h in history]
    return "\n".join(lines)
