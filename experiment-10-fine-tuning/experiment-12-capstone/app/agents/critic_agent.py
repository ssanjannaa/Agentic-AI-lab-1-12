"""
Reflection & Critic Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
from typing import List, Tuple
from app.schemas import SecurityAssessment, ComplianceAudit, ReflectionResult, AgentStepTrace

class ReflectionCriticAgent:
    def __init__(self):
        self.agent_name = "ReflectionCriticAgent"

    def review(self, assessment: SecurityAssessment, audit: ComplianceAudit, max_cycles: int = 1, step_id: int = 6) -> Tuple[ReflectionResult, AgentStepTrace]:
        start = time.time()

        gaps = []
        if not assessment.indicators.get("ip_addresses") and not assessment.indicators.get("domains") and not assessment.indicators.get("cve_ids"):
            gaps.append("No explicit network IOCs or CVE references detected in raw logs.")

        if not assessment.mitre_attack_mappings:
            gaps.append("MITRE ATT&CK technique mapping incomplete for this category.")

        if audit.grounding_status == "INSUFFICIENT_EVIDENCE":
            gaps.append("RAG retrieval produced zero document chunks; consideration for broader keyword search recommended.")

        critic_passed = len(gaps) == 0 or audit.is_defensive_compliant
        feedback = "Quality Audit Passed: Structured analysis is evidence-grounded and defensive." if critic_passed else f"Quality Warning: {'; '.join(gaps)}"

        result = ReflectionResult(
            critic_passed=critic_passed,
            cycles_executed=1,
            identified_gaps=gaps,
            critic_feedback=feedback
        )

        duration_ms = round((time.time() - start) * 1000, 2)
        trace = AgentStepTrace(
            step_id=step_id,
            agent_name=self.agent_name,
            action="Perform Reflection & Quality Review Pass",
            input_summary=f"Max Cycles: {max_cycles}",
            output_summary=f"Critic Passed: {critic_passed} | Gaps Found: {len(gaps)}",
            duration_ms=duration_ms,
            status="REFLECTED"
        )

        return result, trace
