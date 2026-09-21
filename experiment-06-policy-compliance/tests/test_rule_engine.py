"""
Rule Engine Unit Tests
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

from app.services.rule_engine import DeterministicRuleEngine

def test_evaluate_rule_pass():
    engine = DeterministicRuleEngine()
    rule_dict = {
        "rule_id": "RULE-SEC-01A",
        "name": "MFA Enforcement",
        "description": "Multi-Factor Authentication (MFA) must be enforced.",
        "required_keywords": ["mfa", "2fa"],
        "prohibited_actions": ["bypass mfa"],
        "severity": "CRITICAL",
        "remediation": "Enable MFA."
    }
    
    scenario = "We enforced MFA 2FA security keys on all remote VPN access portals."
    eval_res = engine.evaluate_rule(rule_dict, scenario)

    assert eval_res.status == "PASS"
    assert "MFA" in eval_res.matched_keywords or "2fa" in eval_res.matched_keywords

def test_evaluate_rule_fail():
    engine = DeterministicRuleEngine()
    rule_dict = {
        "rule_id": "RULE-PII-02A",
        "name": "PII Encryption",
        "description": "PII must be encrypted.",
        "required_keywords": ["aes-256"],
        "prohibited_actions": ["unencrypted pii", "plaintext pii"],
        "severity": "CRITICAL",
        "remediation": "Encrypt PII."
    }
    
    scenario = "Developer left unencrypted PII customer email addresses in raw log files."
    eval_res = engine.evaluate_rule(rule_dict, scenario)

    assert eval_res.status == "FAIL"
    assert eval_res.severity == "CRITICAL"
