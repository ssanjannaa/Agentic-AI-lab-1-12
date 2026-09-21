"""
Pydantic API Request/Response Schemas
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class IncidentQueryRequest(BaseModel):
    query: str = Field(
        default="Analyze suspicious login attempts and recommend containment playbooks.",
        description="Incident description or cybersecurity query"
    )
    incident_id: Optional[str] = Field(default=None, description="Optional sample incident identifier")
    max_reflection_cycles: Optional[int] = Field(default=1, ge=0, le=2)

class EvidenceItem(BaseModel):
    document_name: str
    chunk_id: str
    content: str
    relevance_score: float
    topics: List[str]

class ToolCallLog(BaseModel):
    tool_name: str
    input_args: Dict[str, Any]
    output_result: Dict[str, Any]
    duration_ms: float

class AgentStepTrace(BaseModel):
    step_id: int
    agent_name: str
    action: str
    input_summary: str
    output_summary: str
    duration_ms: float
    status: str  # "COMPLETED", "VERIFIED", "REFLECTED"

class SecurityAssessment(BaseModel):
    incident_category: str
    severity: str
    indicators: Dict[str, List[str]]
    mitre_attack_mappings: List[Dict[str, str]]
    technical_findings: List[str]
    defensive_recommendations: List[str]

class ComplianceAudit(BaseModel):
    grounding_status: str  # "SUPPORTED", "PARTIALLY_SUPPORTED", "INSUFFICIENT_EVIDENCE"
    is_defensive_compliant: bool
    verified_claims_count: int
    unsupported_claims_count: int
    audit_notes: str

class ReflectionResult(BaseModel):
    critic_passed: bool
    cycles_executed: int
    identified_gaps: List[str]
    critic_feedback: str

class SynthesizedReport(BaseModel):
    executive_summary: str
    technical_assessment: SecurityAssessment
    retrieved_evidence: List[EvidenceItem]
    tool_calls: List[ToolCallLog]
    mitre_mappings: List[Dict[str, str]]
    recommended_defensive_actions: List[str]
    compliance_verification: ComplianceAudit
    reflection_summary: ReflectionResult
    sources: List[str]

class OrchestratorResponse(BaseModel):
    trace_id: str
    query: str
    intent_category: str
    workflow_plan: List[str]
    retrieved_evidence: List[EvidenceItem]
    tool_calls: List[ToolCallLog]
    security_assessment: SecurityAssessment
    compliance_audit: ComplianceAudit
    reflection_result: ReflectionResult
    final_report: SynthesizedReport
    agent_trace: List[AgentStepTrace]
    execution_metrics: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    app: str
    course: str
    port: int
    llm_provider: str
    knowledge_base_documents: int
    sample_incidents_loaded: int
