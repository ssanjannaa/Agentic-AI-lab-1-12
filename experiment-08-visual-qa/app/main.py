"""
FastAPI Server Entry Point & Router
Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
Port: 8007
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from app.config import settings
from app.schemas import SearchRequest, SearchResponse, VisualQARequest, VisualQAResponse, ImageMetadata
from app.services.indexer import load_image_catalog
from app.services.retriever import VisualFeatureRetriever
from app.services.vqa_engine import VisualQAEngine

app = FastAPI(
    title="Experiment 08 — Image Retrieval / Visual QA System",
    description="Multimodal pipeline for visual questioning and image search.",
    version="1.0.0"
)

# Mount static UI assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

retriever = VisualFeatureRetriever()
vqa_engine = VisualQAEngine()

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "app": "Experiment 08 — Image Retrieval / Visual QA System",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "status": "online",
        "port": settings.PORT
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Experiment 08 — Image Retrieval / Visual QA System",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "port": settings.PORT,
        "llm_provider": settings.LLM_PROVIDER,
        "catalog_status": "loaded"
    }

@app.get("/api/images")
async def get_image_catalog() -> List[ImageMetadata]:
    catalog = load_image_catalog()
    return [ImageMetadata(**img) for img in catalog]

@app.post("/api/search", response_model=SearchResponse)
async def search_images(req: SearchRequest):
    try:
        return retriever.search_catalog(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image Search Error: {str(e)}")

@app.post("/api/vqa", response_model=VisualQAResponse)
async def answer_visual_question(req: VisualQARequest):
    try:
        return vqa_engine.answer_question(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Visual QA Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
