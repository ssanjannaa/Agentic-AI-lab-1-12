"""
Quality / Compliance Reviewer Agent
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Audits generated email drafts for personalization, claim validity, tone, and compliance standards.
"""

from typing import Dict, Any
from app.schemas import EmailDraft, ComplianceCheck

class ComplianceReviewerAgent:
    def __init__(self):
        self.agent_name = "Quality & Compliance Reviewer Agent"

    def review_draft(self, lead: Dict[str, Any], draft: EmailDraft) -> ComplianceCheck:
        notes = []
        body = draft.email_body
        subject = draft.subject_line
        
        # 1. Personalization Check
        has_name = lead.get("contact_name", "") in body
        has_company = lead.get("company_name", "") in body
        has_personalization = has_name and has_company
        
        if not has_personalization:
            notes.append("Warning: Email body lacks explicit recipient or company name personalization.")
        else:
            notes.append("Personalization: Recipient name and company name correctly populated.")

        # 2. Unsupported Claims Check
        unsupported_buzzwords = ["guarantee 100%", "zero cost", "instant 10x", "flawless"]
        has_unsupported_claims = any(bw in body.lower() for bw in unsupported_buzzwords)
        
        if has_unsupported_claims:
            notes.append("Violation: Contains unverified or exaggerated guarantee claims.")
        else:
            notes.append("Claims Validation: No unverified or exaggerated claims detected.")

        # 3. Tone & Formatting Assessment
        tone = "Professional B2B Consultative"
        if len(body) < 50:
            tone = "Unusually Brief"
            notes.append("Warning: Email body length is under 50 characters.")
        elif len(body) > 1000:
            tone = "Excessively Long"
            notes.append("Warning: Email body exceeds 1000 characters.")

        # 4. Review Verdict
        is_compliant = has_personalization and not has_unsupported_claims
        if is_compliant:
            verdict = "APPROVED_FOR_SENDING"
        elif has_personalization and has_unsupported_claims:
            verdict = "NEEDS_REVISION"
        else:
            verdict = "REJECTED"

        return ComplianceCheck(
            lead_id=lead["id"],
            is_compliant=is_compliant,
            has_personalization=has_personalization,
            has_unsupported_claims=has_unsupported_claims,
            tone_assessment=tone,
            compliance_notes=notes,
            review_verdict=verdict
        )
