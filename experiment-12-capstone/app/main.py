"""
FastAPI Application Entry Point
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from app.config import settings
from app.schemas import (
    HealthResponse, IncidentQueryRequest, OrchestratorResponse,
    EvidenceItem
)
from app.services.rag_engine import rag_engine
from app.services.tools import IOCParserTool, RiskCalculatorTool
from app.services.orchestrator import orchestrator

app = FastAPI(
    title=settings.APP_NAME,
    description="Capstone Project for Applied Agentic AI Laboratory (MR23-1CS0436)",
    version="1.0.0"
)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": f"Welcome to {settings.APP_NAME}"})

@app.get("/api/health", response_model=HealthResponse)
def get_health():
    stats = rag_engine.get_stats()
    incidents_count = 0
    if os.path.exists(settings.INCIDENTS_FILE):
        with open(settings.INCIDENTS_FILE, "r", encoding="utf-8") as f:
            incidents_count = len(json.load(f))

    return HealthResponse(
        status="healthy",
        app=settings.APP_NAME,
        course=f"Applied Agentic AI Laboratory ({settings.COURSE_CODE})",
        port=settings.PORT,
        llm_provider="local-deterministic-orchestrator",
        knowledge_base_documents=stats["total_documents"],
        sample_incidents_loaded=incidents_count
    )

@app.get("/api/system")
def get_system_info():
    return {
        "app_name": settings.APP_NAME,
        "course_code": settings.COURSE_CODE,
        "port": settings.PORT,
        "rag_chunk_size": settings.CHUNK_SIZE,
        "rag_top_k": settings.TOP_K_RESULTS,
        "agents": [
            "SupervisorAgent",
            "RetrievalAgent",
            "ToolAgent",
            "SecurityAnalysisAgent",
            "ComplianceVerificationAgent",
            "ReflectionCriticAgent",
            "SynthesisAgent"
        ]
    }

@app.get("/api/incidents")
def get_sample_incidents():
    if os.path.exists(settings.INCIDENTS_FILE):
        with open(settings.INCIDENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/api/knowledge/stats")
def get_knowledge_stats():
    return rag_engine.get_stats()

@app.post("/api/analyze", response_model=OrchestratorResponse)
def analyze_incident(req: IncidentQueryRequest):
    if not req.query and not req.incident_id:
        raise HTTPException(status_code=400, detail="Query text or incident_id must be provided.")
    return orchestrator.process_incident(req)

@app.post("/api/retrieve")
def direct_retrieve(query: str, top_k: int = 3):
    if not query:
        raise HTTPException(status_code=400, detail="Query string cannot be empty.")
    items = rag_engine.retrieve(query, top_k=top_k)
    return {"query": query, "top_k": top_k, "results": [item.dict() for item in items]}

@app.post("/api/tools/ioc")
def parse_iocs(raw_text: str):
    if not raw_text:
        raise HTTPException(status_code=400, detail="raw_text cannot be empty.")
    return IOCParserTool.execute(raw_text)

@app.post("/api/tools/risk")
def calculate_risk(impact_score: float, likelihood_score: float, confidence: float = 0.8):
    return RiskCalculatorTool.execute(impact_score, likelihood_score, confidence)

@app.get("/api/trace/{trace_id}")
def get_trace(trace_id: str):
    # Simulated trace retrieval for observability
    return {
        "trace_id": trace_id,
        "status": "COMPLETED",
        "message": f"Execution trace '{trace_id}' successfully recorded in system observability logs."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=settings.PORT, reload=True)
