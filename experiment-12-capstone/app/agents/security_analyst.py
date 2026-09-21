"""
Security Analysis Specialist Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
from typing import List, Dict, Any, Tuple
from app.schemas import EvidenceItem, ToolCallLog, SecurityAssessment, AgentStepTrace

class SecurityAnalysisAgent:
    def __init__(self):
        self.agent_name = "SecurityAnalysisAgent"

    def analyze(self, query: str, category: str, evidence: List[EvidenceItem], tool_logs: List[ToolCallLog], step_id: int = 4) -> Tuple[SecurityAssessment, AgentStepTrace]:
        start = time.time()

        # Extract risk score & severity from tool logs
        risk_score = 7.5
        severity = "HIGH"
        iocs = {"ip_addresses": [], "domains": [], "cve_ids": [], "file_hashes": [], "urls": []}
        mitre_mappings = []
        defensive_recommendations = []

        for log in tool_logs:
            if log.tool_name == "RiskCalculatorTool":
                risk_score = log.output_result.get("risk_score", 7.5)
                severity = log.output_result.get("severity_level", "HIGH")
            elif log.tool_name == "IOCParserTool":
                iocs = log.output_result.get("extracted_iocs", iocs)
            elif log.tool_name == "MITRELookupTool":
                techniques = log.output_result.get("techniques", [])
                controls = log.output_result.get("defensive_controls", [])
                for t in techniques:
                    mitre_mappings.append({"id": t["id"], "name": t["name"], "tactic": log.output_result.get("tactic", "")})
                defensive_recommendations.extend(controls)

        # Synthesize Technical Findings grounded in evidence
        technical_findings = []
        if evidence:
            for ev in evidence:
                technical_findings.append(f"Grounded Knowledge ({ev.document_name}): {ev.content[:140]}...")

        if iocs.get("ip_addresses"):
            technical_findings.append(f"Extracted External IP Indicators: {', '.join(iocs['ip_addresses'])}")
        if iocs.get("domains"):
            technical_findings.append(f"Extracted Suspicious Domains: {', '.join(iocs['domains'])}")
        if iocs.get("cve_ids"):
            technical_findings.append(f"Identified Vulnerability References: {', '.join(iocs['cve_ids'])}")
        if iocs.get("file_hashes"):
            technical_findings.append(f"Identified Malicious Hashes: {', '.join(iocs['file_hashes'])}")

        if not technical_findings:
            technical_findings.append(f"Technical pattern matches '{category}' with calculated risk score {risk_score}/10.")

        # Ensure unique defensive recommendations
        defensive_recommendations = list(dict.fromkeys(defensive_recommendations))
        if not defensive_recommendations:
            defensive_recommendations = [
                "Enforce Multi-Factor Authentication (MFA) across all identity providers.",
                "Isolate affected hosts from internal network subnets.",
                "Block malicious IP and domain indicators at perimeter firewall.",
                "Reset user credentials and terminate active web sessions."
            ]

        assessment = SecurityAssessment(
            incident_category=category,
            severity=severity,
            indicators=iocs,
            mitre_attack_mappings=mitre_mappings,
            technical_findings=technical_findings,
            defensive_recommendations=defensive_recommendations
        )

        duration_ms = round((time.time() - start) * 1000, 2)
        trace = AgentStepTrace(
            step_id=step_id,
            agent_name=self.agent_name,
            action="Perform Technical Security Analysis",
            input_summary=f"Evidence: {len(evidence)} items | Category: {category}",
            output_summary=f"Severity: {severity} | Findings: {len(technical_findings)} | Actions: {len(defensive_recommendations)}",
            duration_ms=duration_ms,
            status="COMPLETED"
        )

        return assessment, trace
