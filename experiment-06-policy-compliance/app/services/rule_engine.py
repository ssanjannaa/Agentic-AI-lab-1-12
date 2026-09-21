"""
Authoritative Deterministic Rule Engine
Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
Evaluates scenario narratives against formal policy rules.
"""

from typing import Dict, Any, List
from app.schemas import RuleEvaluation, PolicyRule

class DeterministicRuleEngine:
    def __init__(self):
        self.engine_name = "Authoritative Policy Rule Engine v1.0"

    def evaluate_rule(self, rule_dict: Dict[str, Any], scenario_text: str) -> RuleEvaluation:
        text_lower = scenario_text.lower()
        rule = PolicyRule(**rule_dict)

        matched_keywords = []
        for kw in rule.required_keywords:
            if kw.lower() in text_lower:
                matched_keywords.append(kw)

        detected_prohibitions = []
        for pa in rule.prohibited_actions:
            # Check for keyword matches of prohibited actions
            pa_words = [w for w in pa.lower().split() if len(w) > 3]
            if any(w in text_lower for w in pa_words):
                detected_prohibitions.append(pa)

        # Explicit check for known non-compliant trigger patterns
        has_prohibition_match = len(detected_prohibitions) > 0 or any(
            bad_term in text_lower for bad_term in ["raw customer email", "unencrypted pii", "http transmission", "paste api key", "bypass mfa"]
        )

        if has_prohibition_match:
            status = "FAIL"
            reason = f"Violation Detected: Scenario matches prohibited action pattern ({', '.join(detected_prohibitions) if detected_prohibitions else 'unencrypted/unauthenticated risk'})."
        elif len(matched_keywords) > 0:
            status = "PASS"
            reason = f"Compliance Verified: Matched mandatory policy controls ({', '.join(matched_keywords)})."
        else:
            status = "WARNING"
            reason = "Partial Evidence: Scenario lacks explicit proof of policy enforcement controls."

        return RuleEvaluation(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            severity=rule.severity,
            status=status,
            reason=reason,
            detected_prohibitions=detected_prohibitions,
            matched_keywords=matched_keywords,
            remediation=rule.remediation if status != "PASS" else "No action required."
        )
