"""
FastAPI Server Entry Point & Router
Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
Port: 8008
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from app.config import settings
from app.schemas import BenchmarkRequest, BenchmarkComparisonResponse, BenchmarkTask
from app.services.benchmark_engine import ReasoningBenchmarkEngine, load_benchmark_tasks

app = FastAPI(
    title="Experiment 09 — Reasoning Model Benchmarking",
    description="Comparative benchmark engine for Direct Answer, Structured Decomposition, Tool-Assisted ReAct, and Multi-Agent strategies.",
    version="1.0.0"
)

# Mount static UI assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

engine = ReasoningBenchmarkEngine()

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "app": "Experiment 09 — Reasoning Model Benchmarking",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "status": "online",
        "port": settings.PORT
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Experiment 09 — Reasoning Model Benchmarking",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "port": settings.PORT,
        "llm_provider": settings.LLM_PROVIDER,
        "benchmark_tasks_status": "loaded"
    }

@app.get("/api/tasks")
@app.get("/api/benchmarks/tasks")
async def get_tasks() -> List[BenchmarkTask]:
    tasks = load_benchmark_tasks()
    return [BenchmarkTask(**t) for t in tasks]

@app.post("/api/benchmark", response_model=BenchmarkComparisonResponse)
@app.post("/api/benchmarks/evaluate", response_model=BenchmarkComparisonResponse)
async def evaluate_benchmark(req: BenchmarkRequest):
    try:
        return engine.run_benchmark(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
