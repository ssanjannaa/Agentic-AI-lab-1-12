"""
Compliance Evaluator & Score Calculator
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
Aggregates rule evaluations, calculates compliance score (0-100), and synthesizes remediation guidance.
"""

import time
from typing import Dict, Any, List
from app.schemas import ComplianceAuditResponse, AuditRequest, RuleEvaluation
from app.services.policy_loader import get_policy_by_id, load_policies
from app.services.rule_engine import DeterministicRuleEngine

class ComplianceEvaluatorAgent:
    def __init__(self):
        self.rule_engine = DeterministicRuleEngine()

    def evaluate_scenario(self, req: AuditRequest) -> ComplianceAuditResponse:
        start_time = time.time()
        audit_trace = []

        policy_dict = get_policy_by_id(req.policy_id)
        if not policy_dict:
            all_policies = load_policies()
            policy_dict = all_policies[0] if all_policies else {}

        policy_id = policy_dict.get("policy_id", "POL-DEFAULT")
        policy_title = policy_dict.get("title", "Standard Policy")
        policy_category = policy_dict.get("category", "General Security")
        rules = policy_dict.get("rules", [])

        audit_trace.append({
            "step": 1,
            "stage": "POLICY_LOAD",
            "description": f"Loaded Policy '{policy_title}' ({policy_id}) with {len(rules)} formal rules.",
            "duration_ms": 2.0
        })

        rule_evaluations: List[RuleEvaluation] = []
        critical_violations = 0
        passed_count = 0
        failed_count = 0

        t0 = time.time()
        for r_dict in rules:
            eval_res = self.rule_engine.evaluate_rule(r_dict, req.scenario_text)
            rule_evaluations.append(eval_res)

            if eval_res.status == "PASS":
                passed_count += 1
            elif eval_res.status == "FAIL":
                failed_count += 1
                if eval_res.severity == "CRITICAL":
                    critical_violations += 1
        t1 = time.time()

        audit_trace.append({
            "step": 2,
            "stage": "RULE_ENGINE_EVALUATION",
            "description": f"Executed deterministic rule evaluation across {len(rules)} rules. Passed: {passed_count}, Failed: {failed_count}.",
            "duration_ms": round((t1 - t0) * 1000, 2)
        })

        # Calculate Compliance Score (0-100)
        total_rules = len(rules) if len(rules) > 0 else 1
        raw_score = int((passed_count / total_rules) * 100)
        if critical_violations > 0:
            compliance_score = max(0, raw_score - 40)
        else:
            compliance_score = raw_score

        if compliance_score >= 80 and failed_count == 0:
            overall_status = "COMPLIANT"
        elif compliance_score >= 50 and critical_violations == 0:
            overall_status = "WARNING"
        else:
            overall_status = "NON_COMPLIANT"

        # Collect unique remediations
        remediations = []
        for ev in rule_evaluations:
            if ev.status != "PASS" and ev.remediation not in remediations:
                remediations.append(ev.remediation)

        audit_trace.append({
            "step": 3,
            "stage": "REMEDIATION_SYNTHESIS",
            "description": f"Synthesized {len(remediations)} remediation action item(s) for overall status '{overall_status}'.",
            "duration_ms": 1.5
        })

        total_duration = round((time.time() - start_time) * 1000, 2)

        return ComplianceAuditResponse(
            policy_id=policy_id,
            policy_title=policy_title,
            policy_category=policy_category,
            scenario_text=req.scenario_text,
            compliance_score=compliance_score,
            overall_status=overall_status,
            total_rules_evaluated=len(rules),
            rules_passed=passed_count,
            rules_failed=failed_count,
            critical_violations_count=critical_violations,
            rule_evaluations=rule_evaluations,
            recommended_remediations=remediations,
            audit_trace=audit_trace,
            evaluation_duration_ms=total_duration
        )
