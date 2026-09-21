"""
Individual Agent Specialist Unit Tests
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

from app.agents.supervisor import SupervisorAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.tool_agent import ToolAgent
from app.agents.security_analyst import SecurityAnalysisAgent
from app.agents.compliance_agent import ComplianceVerificationAgent
from app.agents.critic_agent import ReflectionCriticAgent
from app.agents.synthesis_agent import SynthesisAgent
from app.schemas import EvidenceItem

def test_supervisor_agent_planning():
    sup = SupervisorAgent()
    category, plan, impact, likelihood, trace = sup.plan_workflow("Detect ransomware execution and shadow copy deletion")
    assert category == "Malware / Ransomware"
    assert len(plan) == 8
    assert trace.status == "COMPLETED"

def test_retrieval_agent_execution():
    ra = RetrievalAgent()
    items, trace = ra.execute_retrieval("SQL injection probing", top_k=2)
    assert len(items) > 0
    assert trace.status == "COMPLETED"

def test_tool_agent_execution():
    ta = ToolAgent()
    tool_logs, trace = ta.execute_tools("Brute force login", "Authentication Anomaly", "IP 198.51.100.45", ["EventID 4625"], 7.5, 8.0)
    assert len(tool_logs) >= 4
    assert trace.status == "COMPLETED"

def test_security_analysis_agent():
    sa = SecurityAnalysisAgent()
    evidence = [EvidenceItem(document_name="kb_01_authentication_attacks.md", chunk_id="chunk-1", content="Brute force mitigation", relevance_score=0.8, topics=["Auth"])]
    assessment, trace = sa.analyze("Brute force login", "Authentication Anomaly", evidence, [])
    assert assessment.incident_category == "Authentication Anomaly"
    assert len(assessment.defensive_recommendations) >= 1
    assert trace.status == "COMPLETED"

def test_compliance_verification_agent():
    ca = ComplianceVerificationAgent()
    ra = RetrievalAgent()
    evidence, _ = ra.execute_retrieval("Phishing lure email", top_k=2)
    sa = SecurityAnalysisAgent()
    assessment, _ = sa.analyze("Phishing lure email", "Phishing / Email Security", evidence, [])
    
    audit, trace = ca.verify(assessment, evidence)
    assert audit.grounding_status in ["SUPPORTED", "PARTIALLY_SUPPORTED"]
    assert audit.is_defensive_compliant is True
    assert trace.status == "VERIFIED"

def test_reflection_critic_agent():
    rc = ReflectionCriticAgent()
    sa = SecurityAnalysisAgent()
    assessment, _ = sa.analyze("Web attack", "Web Attack", [], [])
    ca = ComplianceVerificationAgent()
    audit, _ = ca.verify(assessment, [])

    result, trace = rc.review(assessment, audit, max_cycles=1)
    assert result.cycles_executed == 1
    assert trace.status == "REFLECTED"

def test_synthesis_agent():
    sy = SynthesisAgent()
    sa = SecurityAnalysisAgent()
    assessment, _ = sa.analyze("Phishing lure email", "Phishing / Email Security", [], [])
    ca = ComplianceVerificationAgent()
    audit, _ = ca.verify(assessment, [])
    rc = ReflectionCriticAgent()
    reflection, _ = rc.review(assessment, audit)

    report, trace = sy.synthesize("Phishing lure email", assessment, [], [], audit, reflection)
    assert "Executive Summary" in report.executive_summary or len(report.executive_summary) > 20
    assert len(report.recommended_defensive_actions) >= 1
    assert trace.status == "COMPLETED"
