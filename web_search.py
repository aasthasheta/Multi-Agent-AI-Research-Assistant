"""
Lightweight web search used by the Research Agent.

Uses DuckDuckGo's HTML search (via the `duckduckgo-search` package), which
requires no API key. Falls back to returning an empty list on failure so the
rest of the pipeline can still run (e.g. offline demos, rate limits).
"""
from __future__ import annotations
import logging
from app.utils.config import settings

logger = logging.getLogger("web_search")


def search_web(query: str, max_results: int | None = None) -> list[dict]:
    """Return a list of {title, url, snippet} dicts for a web query."""
    max_results = max_results or settings.max_web_results
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", ""),
                    }
                )
        return results
    except Exception:
        logger.exception("Web search failed for query: %s", query)
        return []
