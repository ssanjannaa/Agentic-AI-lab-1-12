"""
FastAPI Application Entry Point & Router
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.schemas import QueryRequest, QueryResponse, IndexRequest, KBStatusResponse, HealthResponse
from app.services.vector_store import global_vector_store
from app.services.rag_service import process_rag_query

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="RAG-Based Question Answering System for Cybersecurity Knowledge Base (MR23-1CS0436)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the main Chatbot Web Interface."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Cybersecurity Knowledge RAG Assistant API is running."}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Returns application health status, course code, and loaded models."""
    status = global_vector_store.get_status()
    return HealthResponse(
        status="healthy",
        app=settings.APP_TITLE,
        course=settings.COURSE_CODE,
        llm_provider=settings.LLM_PROVIDER,
        embedding_model=settings.EMBEDDING_MODEL,
        index_exists=status.get("status") == "ready"
    )

@app.get("/api/knowledge-base/status", response_model=KBStatusResponse)
async def get_kb_status():
    """Returns knowledge base indexing status, document/chunk counts, and last indexed time."""
    try:
        status = global_vector_store.get_status()
        return KBStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve KB status: {str(e)}")

@app.post("/api/index", response_model=KBStatusResponse)
async def rebuild_vector_index(request: IndexRequest):
    """Rebuilds and re-indexes all Markdown documents in data/knowledge_base/."""
    try:
        status = global_vector_store.build_index()
        return KBStatusResponse(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rebuild vector index: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
async def execute_rag_query(request: QueryRequest):
    """
    Executes the 6-step RAG Question Answering Workflow:
    Index Check -> Query Embedding -> Vector Retrieval -> Context Building -> Response Gen -> Grounded Answer
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    if len(request.question) > 500:
        raise HTTPException(status_code=400, detail="Question exceeds maximum allowed length of 500 characters.")

    try:
        response_data = process_rag_query(request.question, top_k=request.top_k or settings.DEFAULT_TOP_K)
        return QueryResponse(**response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing RAG query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
