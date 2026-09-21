"""
Supervisor Orchestrator Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from app.schemas import CampaignRequest
from app.services.sdr_supervisor import SDRSupervisor

def test_supervisor_campaign_workflow():
    supervisor = SDRSupervisor()
    req = CampaignRequest(
        target_industry="Cloud Infrastructure",
        target_region="All",
        min_qualification_threshold=60,
        value_proposition="Cloud Automation"
    )
    
    res = supervisor.run_campaign_workflow(req)

    assert res.leads_discovered_count >= 1
    assert res.leads_qualified_count >= 1
    assert len(res.agent_traces) == 5
    assert res.agent_traces[0].agent_name == "Supervisor -> Lead Discovery Agent"
    assert res.agent_traces[4].agent_name == "Supervisor -> Quality & Compliance Reviewer Agent"
    assert res.workflow_duration_ms > 0

def test_supervisor_empty_discovery():
    supervisor = SDRSupervisor()
    req = CampaignRequest(
        target_industry="NonExistentIndustryXYZ",
        target_region="NonExistentRegionXYZ",
        min_qualification_threshold=60,
        value_proposition="Test Prop"
    )
    
    res = supervisor.run_campaign_workflow(req)

    assert res.leads_discovered_count == 0
    assert res.leads_qualified_count == 0
    assert len(res.email_drafts) == 0
    assert len(res.agent_traces) == 5
