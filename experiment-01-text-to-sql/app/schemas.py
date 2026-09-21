"""
Pydantic API Schemas
Experiment 01 — Text-to-SQL Workflow (MR23-1CS0436)
"""

from typing import List, Any, Dict, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="Natural language question about the university database",
        example="Which department has the most students?"
    )

class WorkflowStep(BaseModel):
    step: str
    status: str  # "pending" | "in_progress" | "completed" | "failed"
    details: Optional[str] = None
    sql: Optional[str] = None
    row_count: Optional[int] = None
    safe: Optional[bool] = None

class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    columns: List[str]
    rows: List[List[Any]]
    explanation: str
    tables_used: List[str]
    reasoning_summary: str
    workflow: List[WorkflowStep]
    provider: str
    success: bool = True
    error: Optional[str] = None

class TableSchemaInfo(BaseModel):
    table_name: str
    columns: List[Dict[str, Any]]
    foreign_keys: List[Dict[str, Any]]
    row_count: int

class SchemaResponse(BaseModel):
    database: str
    table_count: int
    tables: List[TableSchemaInfo]

class HealthResponse(BaseModel):
    status: str
    app: str
    course: str
    llm_provider: str
    database_connected: bool
