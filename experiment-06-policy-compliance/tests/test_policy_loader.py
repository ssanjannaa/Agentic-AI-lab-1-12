"""
Policy Loader Tests
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

from app.services.policy_loader import load_policies, load_scenarios, get_policy_by_id

def test_load_policies():
    policies = load_policies()
    assert len(policies) >= 3
    p_ids = [p["policy_id"] for p in policies]
    assert "POL-SEC-01" in p_ids
    assert "POL-PII-02" in p_ids
    assert "POL-AI-03" in p_ids

def test_load_scenarios():
    scenarios = load_scenarios()
    assert len(scenarios) >= 3
    s_ids = [s["scenario_id"] for s in scenarios]
    assert "SCEN-001" in s_ids

def test_get_policy_by_id():
    policy = get_policy_by_id("POL-SEC-01")
    assert policy is not None
    assert policy["title"] == "Corporate Multi-Factor Authentication & Password Standard"
    assert len(policy["rules"]) >= 2
