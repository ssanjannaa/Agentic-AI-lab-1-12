"""
FastAPI Server Entry Point & Router
Experiment 10 — Fine-Tuning for Domain Adaptation (MR23-1CS0436)
Port: 8009
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Dict, Any, List
import os

from app.config import settings
from app.schemas import FineTuningConfig, TrainingJobResponse, EvalRequest, ModelEvalResponse
from app.services.dataset_curator import DatasetCuratorService
from app.services.trainer import RealLoRATrainer
from app.services.evaluator import ModelEvaluatorService

app = FastAPI(
    title="Experiment 10 — Fine-Tuning for Domain Adaptation",
    description="PEFT/LoRA real PyTorch autograd parameter training and base vs. fine-tuned model evaluation.",
    version="3.0.0"
)

# Mount static UI assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

dataset_curator = DatasetCuratorService()
trainer = RealLoRATrainer()
evaluator = ModelEvaluatorService()

@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({
        "app": "Experiment 10 — Fine-Tuning for Domain Adaptation",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "status": "online",
        "port": settings.PORT
    })

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Experiment 10 — Fine-Tuning for Domain Adaptation",
        "course": "Applied Agentic AI Laboratory (MR23-1CS0436)",
        "port": settings.PORT,
        "llm_provider": settings.LLM_PROVIDER,
        "datasets_status": "loaded"
    }

@app.get("/api/dataset/stats")
@app.get("/api/fine-tuning/dataset")
async def get_dataset_stats():
    return dataset_curator.get_dataset_stats()

@app.post("/api/train/run", response_model=TrainingJobResponse)
@app.post("/api/fine-tuning/train", response_model=TrainingJobResponse)
async def run_training_job(config: FineTuningConfig):
    try:
        return trainer.run_training_job(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training Execution Error: {str(e)}")

@app.post("/api/eval/run", response_model=ModelEvalResponse)
@app.post("/api/fine-tuning/evaluate", response_model=ModelEvalResponse)
async def run_evaluation(req: EvalRequest):
    try:
        return evaluator.evaluate_models(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model Evaluation Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
