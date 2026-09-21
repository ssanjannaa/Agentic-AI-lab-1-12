"""
FastAPI Server Entry Point & Router
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.schemas import QueryRequest, QueryResponse, SchemaResponse, HealthResponse
from app.services.schema_service import get_database_schema_info
from app.services.query_service import process_natural_language_query
from app.database import get_db_path

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Text-to-SQL AI Workflow API for Applied Agentic AI Laboratory (MR23-1CS0436)"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directories
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serves the main Chatbot Web Interface."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "University Database AI Assistant API is running. Please access /api/health or UI."}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Returns application health status, course code, and loaded LLM provider."""
    db_exists = os.path.exists(get_db_path())
    return HealthResponse(
        status="healthy",
        app=settings.APP_TITLE,
        course=settings.COURSE_CODE,
        llm_provider=settings.LLM_PROVIDER,
        database_connected=db_exists
    )

@app.get("/api/schema", response_model=SchemaResponse)
async def get_schema():
    """Returns database schema context including tables, columns, and foreign key relationships."""
    try:
        schema_data = get_database_schema_info()
        return SchemaResponse(**schema_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve database schema: {str(e)}")

@app.post("/api/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    """
    Executes the 6-step Text-to-SQL Agentic Workflow:
    Question -> Schema Retrieval -> Prompt Generation -> Safety Check -> Execution -> Explanation
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="User question cannot be empty.")
    
    try:
        response_data = process_natural_language_query(request.question)
        return QueryResponse(**response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Text-to-SQL request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
