"""
Pydantic API Schemas
Experiment 02 — RAG-Based Question Answering System (MR23-1CS0436)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="Natural language cybersecurity question",
        json_schema_extra={"example": "What is phishing?"}
    )
    top_k: Optional[int] = Field(
        default=4,
        description="Number of relevant document chunks to retrieve",
        ge=1,
        le=10
    )

class SourceEvidence(BaseModel):
    document: str
    chunk_id: str
    score: float
    excerpt: str
    vector_score: Optional[float] = None
    lexical_score: Optional[float] = None

class RAGInspectorMetadata(BaseModel):
    query: str
    normalized_query: Optional[str] = None
    chunks_searched: int
    top_k: int
    max_relevance_score: float
    vector_score: Optional[float] = None
    lexical_score: Optional[float] = None
    embedding_model: str
    vector_store: str
    retrieval_strategy: Optional[str] = "Hybrid (Vector + Lexical)"
    response_mode: str
    out_of_scope: bool

class WorkflowStep(BaseModel):
    step: str
    status: str  # "pending" | "in_progress" | "completed" | "failed"
    details: Optional[str] = None

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceEvidence]
    retrieval_metadata: Dict[str, Any]
    inspector: RAGInspectorMetadata
    workflow: List[WorkflowStep]
    provider: str
    success: bool = True
    error: Optional[str] = None

class IndexRequest(BaseModel):
    force_rebuild: bool = True

class KBStatusResponse(BaseModel):
    status: str
    documents_indexed: int
    chunks_indexed: int
    embedding_model: str
    vector_store: str
    last_indexed: str

class HealthResponse(BaseModel):
    status: str
    app: str
    course: str
    llm_provider: str
    embedding_model: str
    index_exists: bool
