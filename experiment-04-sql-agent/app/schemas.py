"""
Pydantic API Schemas
Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AgentQueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="Natural language database question for the SQL agent",
        min_length=5,
        max_length=2000,
        example="Which department has the highest average employee salary, and how many employees work there?"
    )
    max_iterations: Optional[int] = Field(
        default=8,
        ge=1,
        le=20,
        description="Maximum allowed agent tool loop iterations"
    )

class ToolCallTrace(BaseModel):
    step: int
    decision_summary: str
    tool: str
    arguments: Dict[str, Any]
    observation: str
    status: str  # "success" | "warning" | "error" | "retry" | "completed"
    execution_time_ms: float

class ToolCounter(BaseModel):
    list_tables: int = 0
    get_schema: int = 0
    check_query_syntax: int = 0
    execute_sql: int = 0
    total_calls: int = 0
    retries: int = 0

class AgentQueryResponse(BaseModel):
    question: str
    final_answer: str
    generated_sql: str
    columns: List[str]
    rows: List[List[Any]]
    row_count: int
    tables_used: List[str]
    iterations_used: int
    success: bool
    error: Optional[str] = None
    tool_counters: ToolCounter
    agent_trace: List[ToolCallTrace]
    provider: str

class ValidateRequest(BaseModel):
    sql_query: str = Field(..., description="SQL statement string to validate for read-only safety")

class ValidateResponse(BaseModel):
    is_safe: bool
    error_reason: Optional[str] = None
    cleaned_sql: str

class ColumnSchemaInfo(BaseModel):
    name: str
    type: str
    is_primary_key: bool

class ForeignKeyInfo(BaseModel):
    from_column: str
    to_table: str
    to_column: str

class TableSchemaInfo(BaseModel):
    table_name: str
    columns: List[ColumnSchemaInfo]
    foreign_keys: List[ForeignKeyInfo]
    row_count: int

class DatabaseExplorerResponse(BaseModel):
    database: str
    table_count: int
    tables: List[TableSchemaInfo]

class HealthResponse(BaseModel):
    status: str
    app: str
    course: str
    llm_provider: str
    port: int
    database_status: str
