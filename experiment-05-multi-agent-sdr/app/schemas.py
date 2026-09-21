"""
Pydantic API Request/Response Schemas
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CampaignRequest(BaseModel):
    target_industry: Optional[str] = Field(default="All", description="Target industry to discover leads")
    target_region: Optional[str] = Field(default="All", description="Target region (e.g., North America, Europe)")
    min_qualification_threshold: int = Field(default=60, ge=0, le=100, description="Minimum qualification score (0-100)")
    value_proposition: str = Field(
        default="Enterprise Agentic AI & RAG Automation Platform for reducing operational overhead",
        description="Core value proposition for outbound email personalized outreach"
    )

class LeadFitIndicators(BaseModel):
    tech_match: bool
    decision_maker: bool
    urgency: str

class Lead(BaseModel):
    id: str
    contact_name: str
    contact_role: str
    email: str
    company_name: str
    industry: str
    company_size: str
    region: str
    business_need: str
    engagement_signals: List[str]
    budget_band: str
    tech_stack: List[str]
    fit_indicators: LeadFitIndicators

class QualificationResult(BaseModel):
    lead_id: str
    company_name: str
    fit_score: int
    need_score: int
    intent_score: int
    budget_score: int
    final_score: int
    status: str  # "QUALIFIED" | "DISQUALIFIED"
    qualification_summary: str

class EmailDraft(BaseModel):
    lead_id: str
    recipient_email: str
    subject_line: str
    email_body: str
    value_prop_used: str
    personalized_hook: str
    call_to_action: str

class ComplianceCheck(BaseModel):
    lead_id: str
    is_compliant: bool
    has_personalization: bool
    has_unsupported_claims: bool
    tone_assessment: str
    compliance_notes: List[str]
    review_verdict: str  # "APPROVED_FOR_SENDING" | "NEEDS_REVISION" | "REJECTED"

class AgentStepTrace(BaseModel):
    step: int
    agent_name: str
    action_type: str
    description: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    status: str
    duration_ms: float

class SDRWorkflowResponse(BaseModel):
    campaign_industry: str
    leads_discovered_count: int
    leads_qualified_count: int
    leads: List[Lead]
    qualification_results: List[QualificationResult]
    email_drafts: List[EmailDraft]
    compliance_checks: List[ComplianceCheck]
    agent_traces: List[AgentStepTrace]
    workflow_duration_ms: float
