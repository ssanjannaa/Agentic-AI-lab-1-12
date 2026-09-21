"""
Compliance Evaluator Unit Tests
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
"""

from app.schemas import AuditRequest
from app.services.compliance_evaluator import ComplianceEvaluatorAgent

def test_evaluate_scenario_non_compliant():
    evaluator = ComplianceEvaluatorAgent()
    req = AuditRequest(
        policy_id="POL-PII-02",
        scenario_text="A developer printed raw customer email addresses and unencrypted PII directly to public S3 logs via HTTP transmission."
    )

    res = evaluator.evaluate_scenario(req)

    assert res.overall_status == "NON_COMPLIANT"
    assert res.critical_violations_count > 0
    assert len(res.recommended_remediations) > 0
    assert res.compliance_score < 60

def test_evaluate_scenario_compliant():
    evaluator = ComplianceEvaluatorAgent()
    req = AuditRequest(
        policy_id="POL-SEC-01",
        scenario_text="The security team verified AES-256 encryption, TLS 1.3, and enforced MFA hardware keys with complexity passphrases."
    )

    res = evaluator.evaluate_scenario(req)

    assert res.overall_status in ["COMPLIANT", "WARNING"]
    assert res.rules_passed > 0
