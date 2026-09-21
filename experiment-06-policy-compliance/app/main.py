"""
FastAPI Server Entry Point & Router
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
Port: 8005
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from app.config import settings
from app.schemas import AuditRequest, ComplianceAuditResponse, Policy, AuditScenario
from app.services.policy_loader import load_policies, load_scenarios
from app.services.compliance_evaluator import ComplianceEvaluatorAgent

app = FastAPI(
    title="Experiment 06 — Policy Compliance Agent",
    description="Rule-based compliance evaluation agent for cybersecurity and IT policies.",
    version="1.0.0"
)

# Mount static UI assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

evaluator = ComplianceEvaluatorAgent()

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "app": "Experiment 06 — Policy Compliance Agent",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "status": "online",
        "port": settings.PORT
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Experiment 06 — Policy Compliance Agent",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "port": settings.PORT,
        "llm_provider": settings.LLM_PROVIDER,
        "policies_status": "loaded"
    }

@app.get("/api/policies")
async def get_policies() -> List[Policy]:
    policies_data = load_policies()
    return [Policy(**p) for p in policies_data]

@app.get("/api/scenarios")
async def get_scenarios() -> List[AuditScenario]:
    scenarios_data = load_scenarios()
    return [AuditScenario(**s) for s in scenarios_data]

@app.post("/api/compliance/audit", response_model=ComplianceAuditResponse)
async def evaluate_audit(req: AuditRequest):
    try:
        response = evaluator.evaluate_scenario(req)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance Audit Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
