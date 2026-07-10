"""
FastAPI entry point for the Multi-Agent AI Research Assistant.

Run with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.utils.config import settings

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Multi-Agent AI Research Assistant",
    description="Automates research using planner, research, RAG, verification, "
    "memory, summarization, and report-generation agents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {"status": "ok", "service": "multi-agent-research-assistant"}


@app.get("/health")
def health():
    return {"status": "healthy", "llm_provider": settings.llm_provider}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port, reload=True)
