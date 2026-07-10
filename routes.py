"""
REST API routes for the Multi-Agent Research Assistant.

Endpoints:
    POST /research   - run the full multi-agent pipeline on a query
    POST /upload      - upload a PDF to be embedded into the vector store
    POST /chat         - ask a follow-up question using memory + RAG context
    GET  /report/{id}/{fmt} - download a generated report (md/docx/pdf)
    GET  /status/{task_id}  - check background task status
"""
from __future__ import annotations
import os
import uuid
import shutil
import threading
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.utils.config import settings
from app.utils.llm import chat_completion
from app.rag.ingest import ingest_pdf
from app.rag.vector_store import get_vector_store
from app.agents import memory, rag_agent
from app.graph import run_research_pipeline

router = APIRouter()

# In-memory task registry for the async /research flow.
# For production, replace with Redis/Celery or a DB-backed queue.
_tasks: dict[str, dict] = {}


class ResearchRequest(BaseModel):
    query: str
    session_id: str = "default"
    async_mode: bool = False


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@router.post("/research")
def research(req: ResearchRequest):
    if not req.async_mode:
        try:
            result = run_research_pipeline(req.query, req.session_id)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        return {
            "objectives": result.get("objectives"),
            "summary": result.get("summary"),
            "verification_note": result.get("verification_note"),
            "report_id": result.get("report", {}).get("report_id"),
        }

    task_id = str(uuid.uuid4())
    _tasks[task_id] = {"status": "running", "result": None, "error": None}

    def _run():
        try:
            result = run_research_pipeline(req.query, req.session_id)
            _tasks[task_id] = {
                "status": "complete",
                "result": {
                    "objectives": result.get("objectives"),
                    "summary": result.get("summary"),
                    "report_id": result.get("report", {}).get("report_id"),
                },
                "error": None,
            }
        except Exception as exc:  # pragma: no cover
            _tasks[task_id] = {"status": "failed", "result": None, "error": str(exc)}

    threading.Thread(target=_run, daemon=True).start()
    return {"task_id": task_id, "status": "running"}


@router.get("/status/{task_id}")
def status(task_id: str):
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Unknown task_id")
    return {"task_id": task_id, **task}


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    dest_path = os.path.join(settings.upload_dir, file.filename)
    with open(dest_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        chunks = ingest_pdf(dest_path, source_name=file.filename)
        store = get_vector_store()
        count = store.add_chunks(chunks)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}")

    return {"filename": file.filename, "chunks_indexed": count}


@router.post("/chat")
def chat(req: ChatRequest):
    hits, doc_block = rag_agent.get_document_context(req.message)
    history_block = memory.format_history_block(req.session_id)

    system_prompt = (
        "You are a helpful research assistant answering a follow-up question. "
        "Use the conversation history and any relevant document context provided. "
        "If the context doesn't contain the answer, say so honestly."
    )
    user_prompt = (
        f"Conversation history:\n{history_block}\n\n"
        f"Relevant document context:\n{doc_block}\n\n"
        f"User question: {req.message}"
    )
    try:
        answer = chat_completion(system_prompt, user_prompt, temperature=0.4)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    memory.add_message(req.session_id, "user", req.message)
    memory.add_message(req.session_id, "assistant", answer)
    return {"answer": answer, "sources_used": len(hits)}


@router.get("/report/{report_id}/{fmt}")
def download_report(report_id: str, fmt: str):
    if fmt not in ("md", "docx", "pdf"):
        raise HTTPException(status_code=400, detail="fmt must be one of: md, docx, pdf")
    path = os.path.join(settings.report_dir, f"{report_id}.{fmt}")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path, filename=os.path.basename(path))
