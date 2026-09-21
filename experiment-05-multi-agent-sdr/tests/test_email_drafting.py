"""
Email Drafting Agent Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from app.services.email_drafting_agent import EmailDraftingAgent
from app.services.lead_discovery_agent import load_all_leads

def test_draft_email_generation():
    all_leads = load_all_leads()
    lead = all_leads[0]
    
    drafter = EmailDraftingAgent()
    draft = drafter.draft_email(lead, "AI & RAG Automation Platform")

    assert draft.lead_id == lead["id"]
    assert draft.recipient_email == lead["email"]
    assert lead["contact_name"] in draft.email_body
    assert lead["company_name"] in draft.email_body
    assert "Streamlining" in draft.subject_line
    assert draft.call_to_action != ""
