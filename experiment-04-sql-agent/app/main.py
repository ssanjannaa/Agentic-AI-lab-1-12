"""
FastAPI Server Entry Point & API Router
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)

Port: 8003
URL: http://127.0.0.1:8003
"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.schemas import (
    AgentQueryRequest, AgentQueryResponse,
    ValidateRequest, ValidateResponse,
    DatabaseExplorerResponse, HealthResponse
)
from app.database import get_db_path
from app.services.database_tools import list_tables, get_schema
from app.services.sql_validator import sanitize_and_validate_sql
from app.services.agent_service import run_sql_agent

app = FastAPI(
    title="Autonomous ReAct SQL Agent with Tool Use",
    description="Experiment 04 — Applied Agentic AI Laboratory (MR23-1CS0436)",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=FileResponse)
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Autonomous ReAct SQL Agent API is running."}

@app.get("/api/health", response_model=HealthResponse)
def get_health():
    db_path = get_db_path()
    db_exists = os.path.exists(db_path)
    return HealthResponse(
        status="healthy",
        app="Experiment 04 — Autonomous ReAct SQL Agent with Tool Use",
        course="Applied Agentic AI Laboratory (MR23-1CS0436)",
        llm_provider=settings.LLM_PROVIDER,
        port=settings.PORT,
        database_status="connected" if db_exists else "not_seeded"
    )

@app.get("/api/database/tables")
def get_tables_endpoint():
    return list_tables()

@app.get("/api/database/schema", response_model=DatabaseExplorerResponse)
def get_schema_endpoint():
    info = get_schema()
    return DatabaseExplorerResponse(
        database=info["database"],
        table_count=info["table_count"],
        tables=info["tables"]
    )

@app.post("/api/database/validate", response_model=ValidateResponse)
def validate_sql_endpoint(request: ValidateRequest):
    is_safe, error_reason, cleaned_sql = sanitize_and_validate_sql(request.sql_query)
    return ValidateResponse(
        is_safe=is_safe,
        error_reason=error_reason if not is_safe else None,
        cleaned_sql=cleaned_sql
    )

@app.post("/api/agent/query", response_model=AgentQueryResponse)
def process_agent_query(request: AgentQueryRequest):
    try:
        response = run_sql_agent(request.question, max_iterations=request.max_iterations)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
