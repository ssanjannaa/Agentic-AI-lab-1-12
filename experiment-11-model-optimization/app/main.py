"""
FastAPI Server Entry Point & Router
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
Port: 8010
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from app.config import settings
from app.schemas import OptimizationRequest, OptimizationComparisonResponse
from app.services.optimization_engine import ModelOptimizationEngine

app = FastAPI(
    title="Experiment 11 — Model Optimization Experiment",
    description="Real quantization and knowledge distillation efficiency workbench.",
    version="2.0.0"
)

# Mount static UI assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

engine = ModelOptimizationEngine()

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "app": "Experiment 11 — Model Optimization Experiment",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "status": "online",
        "port": settings.PORT
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Experiment 11 — Model Optimization Experiment",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "port": settings.PORT,
        "llm_provider": settings.LLM_PROVIDER,
        "optimization_engine_status": "ready"
    }

@app.post("/api/optimize", response_model=OptimizationComparisonResponse)
@app.post("/api/optimization/benchmark", response_model=OptimizationComparisonResponse)
async def run_optimization_benchmark(req: OptimizationRequest):
    try:
        return engine.run_optimization_benchmark(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization Benchmark Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
