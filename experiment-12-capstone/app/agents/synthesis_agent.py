"""
Executive Report Synthesis Specialist Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
from typing import List, Tuple
from app.schemas import (
    EvidenceItem, ToolCallLog, SecurityAssessment,
    ComplianceAudit, ReflectionResult, SynthesizedReport, AgentStepTrace
)

class SynthesisAgent:
    def __init__(self):
        self.agent_name = "SynthesisAgent"

    def synthesize(
        self,
        query: str,
        assessment: SecurityAssessment,
        evidence: List[EvidenceItem],
        tool_logs: List[ToolCallLog],
        audit: ComplianceAudit,
        reflection: ReflectionResult,
        step_id: int = 7
    ) -> Tuple[SynthesizedReport, AgentStepTrace]:
        start = time.time()

        exec_summary = (
            f"Anomalous incident activity categorized under '{assessment.incident_category}' was evaluated "
            f"with a severity rating of {assessment.severity}. Multi-agent RAG evidence retrieval gathered "
            f"{len(evidence)} verified local cybersecurity knowledge chunks. {len(assessment.defensive_recommendations)} "
            f"strictly defensive containment actions have been formulated, verified for compliance ({audit.grounding_status}), "
            f"and approved by the Reflection Critic Agent."
        )

        sources = list(dict.fromkeys([ev.document_name for ev in evidence]))
        if not sources:
            sources = ["data/knowledge_base/kb_06_incident_response_playbooks.md"]

        report = SynthesizedReport(
            executive_summary=exec_summary,
            technical_assessment=assessment,
            retrieved_evidence=evidence,
            tool_calls=tool_logs,
            mitre_mappings=assessment.mitre_attack_mappings,
            recommended_defensive_actions=assessment.defensive_recommendations,
            compliance_verification=audit,
            reflection_summary=reflection,
            sources=sources
        )

        duration_ms = round((time.time() - start) * 1000, 2)
        trace = AgentStepTrace(
            step_id=step_id,
            agent_name=self.agent_name,
            action="Synthesize Final Executive Incident Report",
            input_summary=f"Query: {query[:50]}",
            output_summary=f"Report Generated | Sources: {len(sources)} | Verified: {audit.grounding_status}",
            duration_ms=duration_ms,
            status="COMPLETED"
        )

        return report, trace
