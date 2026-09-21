"""
Pydantic API Request/Response Schemas
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PolicyRule(BaseModel):
    rule_id: str
    name: str
    description: str
    required_keywords: List[str]
    prohibited_actions: List[str]
    severity: str  # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    remediation: str

class Policy(BaseModel):
    policy_id: str
    category: str
    title: str
    version: str
    rules: List[PolicyRule]

class AuditScenario(BaseModel):
    scenario_id: str
    title: str
    category: str
    description: str
    target_policy_id: str
    expected_verdict: Optional[str] = None

class AuditRequest(BaseModel):
    policy_id: str = Field(default="POL-PII-02", description="Policy ID to evaluate against")
    scenario_text: str = Field(
        default="A developer committed backend logging middleware that prints raw customer email addresses and unhashed phone numbers directly to public S3 log buckets over HTTP.",
        description="Scenario narrative description to evaluate for policy compliance"
    )

class RuleEvaluation(BaseModel):
    rule_id: str
    rule_name: str
    severity: str
    status: str  # "PASS" | "FAIL" | "WARNING"
    reason: str
    detected_prohibitions: List[str]
    matched_keywords: List[str]
    remediation: str

class ComplianceAuditResponse(BaseModel):
    policy_id: str
    policy_title: str
    policy_category: str
    scenario_text: str
    compliance_score: int  # 0 to 100
    overall_status: str  # "COMPLIANT" | "WARNING" | "NON_COMPLIANT"
    total_rules_evaluated: int
    rules_passed: int
    rules_failed: int
    critical_violations_count: int
    rule_evaluations: List[RuleEvaluation]
    recommended_remediations: List[str]
    audit_trace: List[Dict[str, Any]]
    evaluation_duration_ms: float
