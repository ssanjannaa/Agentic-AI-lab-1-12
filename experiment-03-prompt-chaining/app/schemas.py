"""
Pydantic API Schemas
Experiment 03 — Prompt Chaining for Summarization (MR23-1CS0436)
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        description="Original document text to summarize",
        min_length=30,
        max_length=15000
    )
    summary_style: Optional[str] = Field(
        default="executive",
        description="Style: concise | detailed | executive | bullet | academic"
    )
    summary_length: Optional[str] = Field(
        default="medium",
        description="Length: short | medium | long"
    )

class ChainStageTrace(BaseModel):
    stage: int
    name: str
    purpose: str
    inputs_consumed: List[str]
    status: str  # "pending" | "in_progress" | "completed" | "failed"
    output_preview: str
    execution_time_ms: float

class QualityMetrics(BaseModel):
    original_word_count: int
    final_word_count: int
    compression_ratio: str
    key_points_extracted: int
    important_terms_count: int
    stages_completed: int
    total_processing_time_ms: float

class SummarizeResponse(BaseModel):
    final_summary: str
    draft_summary: str
    key_points: List[str]
    important_terms: List[Dict[str, str]]
    document_analysis: Dict[str, Any]
    critique: Dict[str, Any]
    metrics: QualityMetrics
    chain_trace: List[ChainStageTrace]
    provider: str
    success: bool = True
    error: Optional[str] = None

class SampleDocument(BaseModel):
    id: str
    title: str
    description: str
    content: str

class HealthResponse(BaseModel):
    status: str
    app: str
    course: str
    llm_provider: str

class ModesResponse(BaseModel):
    styles: List[Dict[str, str]]
    lengths: List[Dict[str, str]]
