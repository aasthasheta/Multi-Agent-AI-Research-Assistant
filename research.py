"""
Research Agent
---------------
Searches external knowledge sources (the web) for each planned objective
and collects relevant snippets with their source URLs.
"""
from __future__ import annotations
from app.utils.web_search import search_web


def research(objectives: list[str], results_per_objective: int = 4) -> list[dict]:
    """Run a web search per objective and tag each result with its objective."""
    collected = []
    for objective in objectives:
        hits = search_web(objective, max_results=results_per_objective)
        for hit in hits:
            collected.append({**hit, "objective": objective})
    return collected


def format_research_block(results: list[dict]) -> str:
    if not results:
        return "No external web results were found (web search may be unavailable offline)."
    lines = []
    for i, r in enumerate(results, start=1):
        lines.append(f"[{i}] {r['title']} — {r['url']}\n{r['snippet']}")
    return "\n\n".join(lines)
