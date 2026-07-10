"""
LangGraph orchestration.

Wires the agents together in the documented workflow:

    Planner -> Research -> RAG Retrieval -> Fact Verification
            -> Memory -> Summarization -> Report Generator
"""
from __future__ import annotations
from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.agents import planner, researcher, rag_agent, verifier, summarizer, memory, report_generator


class ResearchState(TypedDict, total=False):
    session_id: str
    query: str
    objectives: list[str]
    research_results: list[dict]
    research_block: str
    document_hits: list[dict]
    document_block: str
    verification_note: str
    summary: str
    report: dict


def planner_node(state: ResearchState) -> ResearchState:
    objectives = planner.plan(state["query"])
    return {"objectives": objectives}


def research_node(state: ResearchState) -> ResearchState:
    results = researcher.research(state["objectives"])
    return {"research_results": results, "research_block": researcher.format_research_block(results)}


def rag_node(state: ResearchState) -> ResearchState:
    hits, block = rag_agent.get_document_context(state["query"])
    return {"document_hits": hits, "document_block": block}


def verify_node(state: ResearchState) -> ResearchState:
    note = verifier.verify(state["research_block"], state["document_block"], state["objectives"])
    return {"verification_note": note}


def memory_node(state: ResearchState) -> ResearchState:
    memory.add_message(state["session_id"], "user", state["query"])
    return {}


def summarize_node(state: ResearchState) -> ResearchState:
    summary = summarizer.summarize(
        state["research_block"], state["document_block"], state["verification_note"], state["query"]
    )
    return {"summary": summary}


def report_node(state: ResearchState) -> ResearchState:
    report = report_generator.generate_report(
        state["query"], state["summary"], state["research_block"], state["document_block"]
    )
    memory.add_message(state["session_id"], "assistant", state["summary"], {"report_id": report["report_id"]})
    return {"report": report}


def build_graph():
    graph = StateGraph(ResearchState)
    graph.add_node("planner", planner_node)
    graph.add_node("research", research_node)
    graph.add_node("rag", rag_node)
    graph.add_node("verify", verify_node)
    graph.add_node("memory", memory_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("report", report_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "research")
    graph.add_edge("research", "rag")
    graph.add_edge("rag", "verify")
    graph.add_edge("verify", "memory")
    graph.add_edge("memory", "summarize")
    graph.add_edge("summarize", "report")
    graph.add_edge("report", END)
    return graph.compile()


_compiled_graph = None


def run_research_pipeline(query: str, session_id: str = "default") -> ResearchState:
    """Entry point used by the API layer: runs the full agent pipeline for a query."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    initial_state: ResearchState = {"session_id": session_id, "query": query}
    final_state = _compiled_graph.invoke(initial_state)
    return final_state
