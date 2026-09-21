"""
FastAPI Server Entry Point & Router
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Port: 8004
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from app.config import settings
from app.schemas import CampaignRequest, SDRWorkflowResponse, Lead
from app.services.lead_discovery_agent import load_all_leads
from app.services.sdr_supervisor import SDRSupervisor

app = FastAPI(
    title="Experiment 05 — Multi-Agent SDR System",
    description="Multi-Agent outbound sales development workflow featuring Lead Discovery, Enrichment, Scoring, Email Drafting, and Quality Review.",
    version="1.0.0"
)

# Mount static web UI assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

supervisor = SDRSupervisor()

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "app": "Experiment 05 — Multi-Agent SDR System",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "status": "online",
        "port": settings.PORT
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Experiment 05 — Multi-Agent SDR System",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "port": settings.PORT,
        "llm_provider": settings.LLM_PROVIDER,
        "leads_dataset_status": "loaded"
    }

@app.get("/api/leads")
async def get_all_leads() -> List[Lead]:
    leads_data = load_all_leads()
    return [Lead(**l) for l in leads_data]

@app.post("/api/sdr/campaign", response_model=SDRWorkflowResponse)
async def run_sdr_campaign(req: CampaignRequest):
    try:
        response = supervisor.run_campaign_workflow(req)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SDR Workflow Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
