"""
Supervisor / Orchestrator Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
import re
from typing import Dict, List, Any
from app.schemas import AgentStepTrace

class SupervisorAgent:
    def __init__(self):
        self.agent_name = "SupervisorAgent"

    def plan_workflow(self, query: str, raw_logs: List[str] = None) -> Tuple_Plan:
        start = time.time()
        query_lower = query.lower()
        logs_str = " ".join(raw_logs).lower() if raw_logs else ""
        combined_text = query_lower + " " + logs_str

        # Classify Incident Intent Category
        if any(w in combined_text for w in ["phish", "email", "mail", "dmarc", "spf", "lure"]):
            category = "Phishing / Email Security"
            default_impact, default_likelihood = 8.5, 9.0
        elif any(w in combined_text for w in ["sql", "sqli", "union select", "xss", "waf", "http 500", "web"]):
            category = "Web Attack"
            default_impact, default_likelihood = 8.0, 8.5
        elif any(w in combined_text for w in ["ransom", "shadow", "vssadmin", "malware", "hash", "edr", "encrypt"]):
            category = "Malware / Ransomware"
            default_impact, default_likelihood = 9.5, 9.0
        elif any(w in combined_text for w in ["exfil", "traffic", "netflow", "outbound", "gb", "dlp", "data transfer"]):
            category = "Data Exfiltration"
            default_impact, default_likelihood = 8.5, 8.0
        else:
            category = "Authentication Anomaly"
            default_impact, default_likelihood = 7.5, 8.0

        plan = [
            f"1. Classify incident intent as '{category}'",
            "2. Retrieve relevant local cybersecurity knowledge base chunks via RAG Retrieval Agent",
            "3. Extract indicators of compromise (IOCs) and raw telemetry using Tool Agent",
            "4. Calculate risk score and lookup MITRE ATT&CK defensive mappings",
            "5. Execute Security Analysis Agent for technical findings and evidence-grounded assessment",
            "6. Execute Compliance Verification Agent to audit evidence grounding and safety rules",
            "7. Run Reflection Critic Agent for quality audit and gap inspection",
            "8. Synthesize final Executive Assessment, Technical Report, and Defensive Mitigation Plan"
        ]

        duration_ms = round((time.time() - start) * 1000, 2)
        trace = AgentStepTrace(
            step_id=1,
            agent_name=self.agent_name,
            action="Generate Execution Plan & Classify Intent",
            input_summary=query[:80],
            output_summary=f"Intent: {category} | Plan: 8 Stages",
            duration_ms=duration_ms,
            status="COMPLETED"
        )

        return category, plan, default_impact, default_likelihood, trace

Tuple_Plan = Any
