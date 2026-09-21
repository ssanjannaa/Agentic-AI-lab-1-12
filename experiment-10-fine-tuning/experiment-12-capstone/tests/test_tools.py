"""
Safe Cybersecurity Tools Unit Tests
Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
"""

from app.services.tools import (
    IOCParserTool, RiskCalculatorTool,
    MITRELookupTool, IncidentTimelineBuilderTool, KnowledgeSearchTool
)

def test_ioc_parser_tool():
    sample_log = "Server 198.51.100.45 hit CVE-2023-23397 and connected to https://malicious-domain.com with hash e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    res = IOCParserTool.execute(sample_log)
    assert res["tool_name"] == "IOCParserTool"
    iocs = res["extracted_iocs"]
    assert "198.51.100.45" in iocs["ip_addresses"]
    assert "malicious-domain.com" in iocs["domains"]
    assert "CVE-2023-23397" in iocs["cve_ids"]
    assert "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" in iocs["file_hashes"]
    assert res["total_extracted"] >= 4

def test_risk_calculator_tool():
    res_critical = RiskCalculatorTool.execute(impact_score=9.0, likelihood_score=9.5, confidence=0.9, asset_criticality=1.0)
    assert res_critical["severity_level"] == "CRITICAL"
    assert res_critical["risk_score"] >= 7.5

    res_low = RiskCalculatorTool.execute(impact_score=2.0, likelihood_score=2.0, confidence=0.5, asset_criticality=0.5)
    assert res_low["severity_level"] == "LOW"

def test_mitre_lookup_tool():
    res = MITRELookupTool.execute("Authentication Anomaly")
    assert res["tool_name"] == "MITRELookupTool"
    assert "techniques" in res
    assert len(res["techniques"]) >= 1
    assert "defensive_controls" in res

def test_incident_timeline_builder_tool():
    raw_logs = [
        "2026-08-11T03:14:02Z EventID=4625 Failed login",
        "2026-08-11T03:17:15Z EventID=4624 Successful login"
    ]
    res = IncidentTimelineBuilderTool.execute(raw_logs)
    assert res["tool_name"] == "IncidentTimelineBuilderTool"
    assert res["total_events"] == 2
    assert res["timeline"][0]["timestamp"] == "2026-08-11T03:14:02Z"

def test_knowledge_search_tool():
    res = KnowledgeSearchTool.execute("ransomware shadow copy", top_k=2)
    assert res["tool_name"] == "KnowledgeSearchTool"
    assert res["results_count"] > 0
