"""
Planner Agent
-------------
Understands the research query and breaks it into a short list of concrete
sub-objectives that the Research and RAG agents will investigate.
"""
from __future__ import annotations
import json
from app.utils.llm import chat_completion

SYSTEM_PROMPT = (
    "You are a meticulous research planner. Given a user's research request, "
    "break it into 3-5 concrete, non-overlapping sub-objectives that together "
    "cover the topic thoroughly. Respond ONLY with a JSON array of short strings, "
    "no prose, no markdown fences."
)


def plan(query: str) -> list[str]:
    raw = chat_completion(SYSTEM_PROMPT, f"Research request: {query}", temperature=0.2)
    cleaned = raw.strip().strip("`")
    if cleaned.lower().startswith("json"):
        cleaned = cleaned[4:].strip()
    try:
        objectives = json.loads(cleaned)
        if isinstance(objectives, list) and objectives:
            return [str(o) for o in objectives]
    except json.JSONDecodeError:
        pass
    # Fallback: split on newlines if the model didn't return clean JSON
    lines = [l.strip("-* \t") for l in raw.splitlines() if l.strip()]
    return lines[:5] if lines else [query]
