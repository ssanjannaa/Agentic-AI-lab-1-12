"""
Quality & Compliance Reviewer Agent Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from app.services.email_drafting_agent import EmailDraftingAgent
from app.services.compliance_reviewer_agent import ComplianceReviewerAgent
from app.services.lead_discovery_agent import load_all_leads

def test_compliance_review_valid():
    all_leads = load_all_leads()
    lead = all_leads[0]
    
    drafter = EmailDraftingAgent()
    reviewer = ComplianceReviewerAgent()

    draft = drafter.draft_email(lead, "AI & RAG Automation Platform")
    check = reviewer.review_draft(lead, draft)

    assert check.is_compliant is True
    assert check.has_personalization is True
    assert check.has_unsupported_claims is False
    assert check.review_verdict == "APPROVED_FOR_SENDING"

def test_compliance_review_unsupported_claim():
    all_leads = load_all_leads()
    lead = all_leads[0]
    
    drafter = EmailDraftingAgent()
    reviewer = ComplianceReviewerAgent()

    draft = drafter.draft_email(lead, "AI Platform")
    # Inject unsupported claim into body
    draft.email_body += " We guarantee 100% instant ROI."

    check = reviewer.review_draft(lead, draft)

    assert check.has_unsupported_claims is True
    assert check.is_compliant is False
    assert check.review_verdict == "NEEDS_REVISION"
