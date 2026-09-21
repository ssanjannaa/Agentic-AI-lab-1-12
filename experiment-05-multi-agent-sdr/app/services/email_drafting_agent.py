"""
Email Drafting Agent
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Generates personalized outbound cold outreach email previews for qualified B2B leads.
SAFE DRAFT ONLY — No real email delivery.
"""

from typing import Dict, Any
from app.schemas import EmailDraft

class EmailDraftingAgent:
    def __init__(self):
        self.agent_name = "Email Drafting Agent"

    def draft_email(self, lead: Dict[str, Any], value_proposition: str) -> EmailDraft:
        contact_name = lead.get("contact_name", "Team")
        company_name = lead.get("company_name", "your company")
        contact_role = lead.get("contact_role", "Leader")
        business_need = lead.get("business_need", "improving operational workflows")
        signals = lead.get("engagement_signals", ["recent activity"])

        signal_str = signals[0] if signals else "your team's recent activity"
        hook = f"I noticed {company_name}'s focus on {business_need.lower()} following {signal_str.lower()}."
        
        subject = f"Streamlining {business_need[:35]}... for {company_name}"
        
        body = (
            f"Hi {contact_name},\n\n"
            f"{hook}\n\n"
            f"As {contact_role} at {company_name}, scaling efficiency while managing technical complexity is critical. "
            f"Our platform ({value_proposition}) helps organizations like yours address these exact challenges with measurable accuracy.\n\n"
            f"Would you be open to a 15-minute briefing next Tuesday to explore how this aligns with {company_name}'s roadmap?\n\n"
            f"Best regards,\n"
            f"Applied Agentic AI SDR Team"
        )
        
        cta = "15-minute briefing request for next Tuesday"

        return EmailDraft(
            lead_id=lead["id"],
            recipient_email=lead.get("email", "contact@company.com"),
            subject_line=subject,
            email_body=body,
            value_prop_used=value_proposition,
            personalized_hook=hook,
            call_to_action=cta
        )
