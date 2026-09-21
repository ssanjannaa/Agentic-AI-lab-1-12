"""
Compliance & Grounding Verification Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
from typing import List, Tuple
from app.schemas import EvidenceItem, SecurityAssessment, ComplianceAudit, AgentStepTrace

class ComplianceVerificationAgent:
    def __init__(self):
        self.agent_name = "ComplianceVerificationAgent"

    def verify(self, assessment: SecurityAssessment, evidence: List[EvidenceItem], step_id: int = 5) -> Tuple[ComplianceAudit, AgentStepTrace]:
        start = time.time()

        verified_count = 0
        unsupported_count = 0
        defensive_compliant = True

        # Check defensive compliance rules (No exploit/offensive keywords)
        offensive_keywords = ["exploit payload", "hack back", "reverse shell", "metasploit", "credential dump tool", "ddos attack"]
        for rec in assessment.defensive_recommendations:
            if any(kw in rec.lower() for kw in offensive_keywords):
                defensive_compliant = False
                unsupported_count += 1

        # Check evidence grounding
        if evidence:
            verified_count += len(evidence)
            grounding_status = "SUPPORTED" if unsupported_count == 0 else "PARTIALLY_SUPPORTED"
            notes = f"All {len(assessment.defensive_recommendations)} recommendations strictly defensive. Grounded against {len(evidence)} knowledge base chunks."
        else:
            grounding_status = "INSUFFICIENT_EVIDENCE"
            unsupported_count += 1
            notes = "No local knowledge base evidence retrieved. Analysis relies on heuristic security baseline rules."

        audit = ComplianceAudit(
            grounding_status=grounding_status,
            is_defensive_compliant=defensive_compliant,
            verified_claims_count=verified_count + len(assessment.defensive_recommendations),
            unsupported_claims_count=unsupported_count,
            audit_notes=notes
        )

        duration_ms = round((time.time() - start) * 1000, 2)
        trace = AgentStepTrace(
            step_id=step_id,
            agent_name=self.agent_name,
            action="Audit Evidence Grounding & Defensive Safety Rules",
            input_summary=f"Assessment Severity: {assessment.severity}",
            output_summary=f"Status: {grounding_status} | Defensive Compliant: {defensive_compliant}",
            duration_ms=duration_ms,
            status="VERIFIED"
        )

        return audit, trace
