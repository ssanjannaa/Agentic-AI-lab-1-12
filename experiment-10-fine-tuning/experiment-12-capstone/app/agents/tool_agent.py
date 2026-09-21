"""
Tool Execution Specialist Agent
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
from typing import List, Dict, Any, Tuple
from app.schemas import ToolCallLog, AgentStepTrace
from app.services.tools import IOCParserTool, RiskCalculatorTool, MITRELookupTool, IncidentTimelineBuilderTool

class ToolAgent:
    def __init__(self):
        self.agent_name = "ToolAgent"

    def execute_tools(self, query: str, category: str, raw_text: str, raw_logs: List[str], impact: float, likelihood: float, step_id: int = 3) -> Tuple[List[ToolCallLog], AgentStepTrace]:
        start = time.time()
        tool_logs: List[ToolCallLog] = []

        # 1. IOC Parser Tool
        full_text = query + " " + raw_text + " " + " ".join(raw_logs)
        t1_start = time.time()
        ioc_res = IOCParserTool.execute(full_text)
        t1_dur = round((time.time() - t1_start) * 1000, 2)
        tool_logs.append(ToolCallLog(
            tool_name="IOCParserTool",
            input_args={"raw_text_length": len(full_text)},
            output_result=ioc_res,
            duration_ms=t1_dur
        ))

        # 2. Risk Calculator Tool
        t2_start = time.time()
        risk_res = RiskCalculatorTool.execute(impact_score=impact, likelihood_score=likelihood, confidence=0.85, asset_criticality=1.0)
        t2_dur = round((time.time() - t2_start) * 1000, 2)
        tool_logs.append(ToolCallLog(
            tool_name="RiskCalculatorTool",
            input_args={"impact": impact, "likelihood": likelihood},
            output_result=risk_res,
            duration_ms=t2_dur
        ))

        # 3. MITRE Lookup Tool
        t3_start = time.time()
        mitre_res = MITRELookupTool.execute(category)
        t3_dur = round((time.time() - t3_start) * 1000, 2)
        tool_logs.append(ToolCallLog(
            tool_name="MITRELookupTool",
            input_args={"category": category},
            output_result=mitre_res,
            duration_ms=t3_dur
        ))

        # 4. Incident Timeline Builder Tool (if logs supplied)
        if raw_logs:
            t4_start = time.time()
            timeline_res = IncidentTimelineBuilderTool.execute(raw_logs)
            t4_dur = round((time.time() - t4_start) * 1000, 2)
            tool_logs.append(ToolCallLog(
                tool_name="IncidentTimelineBuilderTool",
                input_args={"log_count": len(raw_logs)},
                output_result=timeline_res,
                duration_ms=t4_dur
            ))

        duration_ms = round((time.time() - start) * 1000, 2)
        trace = AgentStepTrace(
            step_id=step_id,
            agent_name=self.agent_name,
            action="Execute Safe Cybersecurity Tools",
            input_summary=f"Category: {category}",
            output_summary=f"Executed {len(tool_logs)} tools (IOCs, Risk, MITRE, Timeline)",
            duration_ms=duration_ms,
            status="COMPLETED"
        )

        return tool_logs, trace
