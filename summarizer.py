"""
Summarization Agent
--------------------
Extracts key insights from all gathered material and produces a concise,
de-duplicated summary that feeds into the final report.
"""
from __future__ import annotations
from app.utils.llm import chat_completion

SYSTEM_PROMPT = (
    "You are an expert research summarizer. Combine the web research, "
    "document context, and fact-verification notes you're given into a "
    "clear, well-organized summary of key insights. Remove redundancy. "
    "Use short paragraphs. Do not invent sources."
)


def summarize(research_block: str, document_block: str, verification_note: str, query: str) -> str:
    user_prompt = (
        f"Original research query: {query}\n\n"
        f"Web research:\n{research_block}\n\n"
        f"Document context:\n{document_block}\n\n"
        f"Fact-verification notes:\n{verification_note}\n\n"
        "Write the key-insights summary now."
    )
    return chat_completion(SYSTEM_PROMPT, user_prompt, temperature=0.3, max_tokens=900)
