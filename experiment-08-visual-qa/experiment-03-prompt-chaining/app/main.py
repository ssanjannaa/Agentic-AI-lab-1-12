"""
FastAPI Application Entry Point & Router
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

import os
import glob
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.schemas import SummarizeRequest, SummarizeResponse, HealthResponse, ModesResponse, SampleDocument
from app.services.chain_service import execute_prompt_chain

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Agentic Document Summarization Studio using 6-Stage Sequential Prompt Chaining (MR23-1CS0436)"
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
    """Serves the main Summarization Studio Web Interface."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Agentic Document Summarization Studio API is running."}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Returns application health status and loaded provider."""
    return HealthResponse(
        status="healthy",
        app=settings.APP_TITLE,
        course=settings.COURSE_CODE,
        llm_provider=settings.LLM_PROVIDER
    )

@app.get("/api/modes", response_model=ModesResponse)
async def get_modes():
    """Returns available summary styles and length choices."""
    styles = [
        {"id": "executive", "name": "Executive Summary", "description": "High-level strategic briefing."},
        {"id": "concise", "name": "Concise Summary", "description": "Short, core overview."},
        {"id": "detailed", "name": "Detailed Summary", "description": "Comprehensive section-by-section synthesis."},
        {"id": "bullet", "name": "Bullet-Point Summary", "description": "Structured bullet list."},
        {"id": "academic", "name": "Academic Abstract", "description": "Formal research paper abstract."}
    ]
    lengths = [
        {"id": "short", "name": "Short", "description": "100 - 150 words"},
        {"id": "medium", "name": "Medium", "description": "200 - 300 words"},
        {"id": "long", "name": "Long", "description": "400+ words"}
    ]
    return ModesResponse(styles=styles, lengths=lengths)

@app.get("/api/samples")
async def get_sample_document(id: str = Query(..., description="Sample ID e.g. 01_agentic_ai_paradigms")):
    """Returns content of a pre-loaded educational sample document."""
    sample_path = os.path.join(settings.SAMPLES_DIR, f"{id}.md")
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail=f"Sample document '{id}' not found.")

    with open(sample_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    title = id.replace("_", " ").title()
    lines = content.splitlines()
    if lines and lines[0].startswith("# "):
        title = lines[0].replace("# ", "").strip()

    return SampleDocument(
        id=id,
        title=title,
        description=f"Educational Sample Document ({title})",
        content=content
    )

@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_document(request: SummarizeRequest):
    """
    Executes the 6-Stage Sequential Prompt Chain:
    Stage 1: Document Analysis -> Stage 2: Key Extraction -> Stage 3: Draft Summary ->
    Stage 4: Summary Critique -> Stage 5: Summary Refinement -> Stage 6: Final Output
    """
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")

    if len(text) < 30:
        raise HTTPException(status_code=400, detail="Document text is too short to summarize (minimum 30 characters required).")

    if len(text) > 15000:
        raise HTTPException(status_code=400, detail="Document text exceeds maximum allowed limit of 15,000 characters.")

    style = request.summary_style or settings.DEFAULT_SUMMARY_STYLE
    length = request.summary_length or settings.DEFAULT_SUMMARY_LENGTH

    try:
        response_data = execute_prompt_chain(text, style=style, length=length)
        return SummarizeResponse(**response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing prompt chain: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
