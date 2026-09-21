"""
Lead Discovery Agent Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from app.services.lead_discovery_agent import LeadDiscoveryAgent

def test_discover_all_leads():
    agent = LeadDiscoveryAgent()
    leads = agent.discover_leads("All", "All")
    assert len(leads) >= 6
    ids = [l["id"] for l in leads]
    assert "LEAD-101" in ids
    assert "LEAD-102" in ids

def test_discover_by_industry():
    agent = LeadDiscoveryAgent()
    leads = agent.discover_leads("Cybersecurity", "All")
    assert len(leads) >= 1
    assert leads[0]["company_name"] == "SecureSphere Cyber"

def test_discover_by_region():
    agent = LeadDiscoveryAgent()
    leads = agent.discover_leads("All", "Europe")
    assert len(leads) >= 2
    regions = [l["region"] for l in leads]
    assert any("Europe" in r for r in regions)
