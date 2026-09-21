"""
Lead Qualification Agent
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Evaluates B2B leads across 4 transparent scoring dimensions: Fit, Need, Intent, and Budget.
"""

from typing import Dict, Any
from app.schemas import QualificationResult

class LeadQualificationAgent:
    def __init__(self):
        self.agent_name = "Lead Qualification Agent"

    def qualify_lead(self, lead: Dict[str, Any], min_threshold: int = 60) -> QualificationResult:
        enrichment = lead.get("enrichment_metadata", {})
        fit_ind = lead.get("fit_indicators", {})
        
        # 1. Fit Score (Max 25)
        fit_score = 0
        if enrichment.get("is_executive_role", False):
            fit_score += 15
        elif fit_ind.get("decision_maker", False):
            fit_score += 10
        if fit_ind.get("tech_match", False):
            fit_score += 10

        # 2. Need Score (Max 25)
        need_score = 0
        need = lead.get("business_need", "").lower()
        if any(w in need for w in ["automate", "orchestration", "triage", "rag", "reduce", "accelerat"]):
            need_score += 25
        elif len(need) > 15:
            need_score += 15
        else:
            need_score += 5

        # 3. Intent Score (Max 25)
        intent_score = 0
        intensity = enrichment.get("engagement_intensity_percent", 0)
        intent_score = int(min(intensity * 0.25, 25))
        if fit_ind.get("urgency") == "Critical":
            intent_score = 25
        elif fit_ind.get("urgency") == "High":
            intent_score = max(intent_score, 20)

        # 4. Budget Score (Max 25)
        budget_band = lead.get("budget_band", "")
        budget_score = 0
        if "$100,000+" in budget_band:
            budget_score = 25
        elif "$50,000" in budget_band:
            budget_score = 20
        elif "$30,000" in budget_band:
            budget_score = 15
        elif "$15,000" in budget_band:
            budget_score = 10
        else:
            budget_score = 5

        final_score = fit_score + need_score + intent_score + budget_score
        status = "QUALIFIED" if final_score >= min_threshold else "DISQUALIFIED"

        summary = f"Scored {final_score}/100 (Fit: {fit_score}, Need: {need_score}, Intent: {intent_score}, Budget: {budget_score}). Status: {status}."

        return QualificationResult(
            lead_id=lead["id"],
            company_name=lead["company_name"],
            fit_score=fit_score,
            need_score=need_score,
            intent_score=intent_score,
            budget_score=budget_score,
            final_score=final_score,
            status=status,
            qualification_summary=summary
        )
