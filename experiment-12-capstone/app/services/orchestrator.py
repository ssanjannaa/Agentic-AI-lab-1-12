"""
Multi-Agent System Orchestrator
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

import time
import uuid
import json
import os
from typing import Dict, List, Any, Optional
from app.config import settings
from app.schemas import OrchestratorResponse, AgentStepTrace, IncidentQueryRequest
from app.agents.supervisor import SupervisorAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.tool_agent import ToolAgent
from app.agents.security_analyst import SecurityAnalysisAgent
from app.agents.compliance_agent import ComplianceVerificationAgent
from app.agents.critic_agent import ReflectionCriticAgent
from app.agents.synthesis_agent import SynthesisAgent

class AgenticOrchestrator:
    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.retrieval_agent = RetrievalAgent()
        self.tool_agent = ToolAgent()
        self.security_analyst = SecurityAnalysisAgent()
        self.compliance_agent = ComplianceVerificationAgent()
        self.critic_agent = ReflectionCriticAgent()
        self.synthesis_agent = SynthesisAgent()

    def process_incident(self, req: IncidentQueryRequest) -> OrchestratorResponse:
        start_time = time.time()
        trace_id = f"TRC-{uuid.uuid4().hex[:8].upper()}"

        query = req.query
        raw_logs: List[str] = []
        raw_text = ""

        # Load sample incident data if matching incident_id supplied
        if req.incident_id and os.path.exists(settings.INCIDENTS_FILE):
            with open(settings.INCIDENTS_FILE, "r", encoding="utf-8") as f:
                incidents = json.load(f)
                for inc in incidents:
                    if inc.get("id") == req.incident_id:
                        query = f"{inc.get('title')}: {inc.get('description')}"
                        raw_logs = inc.get("raw_logs", [])
                        raw_text = inc.get("description", "")
                        break

        agent_trace: List[AgentStepTrace] = []

        # 1. Supervisor Agent Workflow Planning
        category, plan, impact, likelihood, t1 = self.supervisor.plan_workflow(query, raw_logs)
        agent_trace.append(t1)

        # 2. Retrieval Agent (RAG Evidence)
        evidence, t2 = self.retrieval_agent.execute_retrieval(query, top_k=settings.TOP_K_RESULTS, step_id=2)
        agent_trace.append(t2)

        # 3. Tool Agent (Safe Cybersecurity Tools)
        tool_logs, t3 = self.tool_agent.execute_tools(query, category, raw_text, raw_logs, impact, likelihood, step_id=3)
        agent_trace.append(t3)

        # 4. Security Analysis Agent
        assessment, t4 = self.security_analyst.analyze(query, category, evidence, tool_logs, step_id=4)
        agent_trace.append(t4)

        # 5. Compliance Verification Agent
        audit, t5 = self.compliance_agent.verify(assessment, evidence, step_id=5)
        agent_trace.append(t5)

        # 6. Reflection Critic Agent
        reflection, t6 = self.critic_agent.review(assessment, audit, max_cycles=req.max_reflection_cycles or 1, step_id=6)
        agent_trace.append(t6)

        # 7. Synthesis Agent (Final Executive Report)
        report, t7 = self.synthesis_agent.synthesize(query, assessment, evidence, tool_logs, audit, reflection, step_id=7)
        agent_trace.append(t7)

        total_duration_ms = round((time.time() - start_time) * 1000, 2)

        metrics = {
            "total_execution_time_ms": total_duration_ms,
            "agents_executed_count": len(agent_trace),
            "tools_called_count": len(tool_logs),
            "evidence_chunks_retrieved": len(evidence),
            "compliance_grounding_status": audit.grounding_status,
            "critic_passed": reflection.critic_passed,
            "defensive_safety_verified": audit.is_defensive_compliant
        }

        return OrchestratorResponse(
            trace_id=trace_id,
            query=query,
            intent_category=category,
            workflow_plan=plan,
            retrieved_evidence=evidence,
            tool_calls=tool_logs,
            security_assessment=assessment,
            compliance_audit=audit,
            reflection_result=reflection,
            final_report=report,
            agent_trace=agent_trace,
            execution_metrics=metrics
        )

orchestrator = AgenticOrchestrator()
