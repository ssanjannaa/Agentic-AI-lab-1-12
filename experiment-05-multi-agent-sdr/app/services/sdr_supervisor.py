"""
Supervisor Orchestrator Agent
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
Coordinates 5 specialized sub-agents in a multi-agent SDR workflow pipeline.
"""

import time
from typing import List, Dict, Any
from app.schemas import (
    CampaignRequest, Lead, QualificationResult, EmailDraft, 
    ComplianceCheck, AgentStepTrace, SDRWorkflowResponse
)
from app.services.lead_discovery_agent import LeadDiscoveryAgent
from app.services.lead_enrichment_agent import LeadEnrichmentAgent
from app.services.lead_qualification_agent import LeadQualificationAgent
from app.services.email_drafting_agent import EmailDraftingAgent
from app.services.compliance_reviewer_agent import ComplianceReviewerAgent

class SDRSupervisor:
    def __init__(self):
        self.discovery_agent = LeadDiscoveryAgent()
        self.enrichment_agent = LeadEnrichmentAgent()
        self.qualification_agent = LeadQualificationAgent()
        self.drafting_agent = EmailDraftingAgent()
        self.reviewer_agent = ComplianceReviewerAgent()

    def run_campaign_workflow(self, req: CampaignRequest) -> SDRWorkflowResponse:
        start_time = time.time()
        traces: List[AgentStepTrace] = []
        step_counter = 1

        # 1. Lead Discovery Step
        t0 = time.time()
        raw_leads = self.discovery_agent.discover_leads(req.target_industry, req.target_region)
        t1 = time.time()

        traces.append(AgentStepTrace(
            step=step_counter,
            agent_name="Supervisor -> Lead Discovery Agent",
            action_type="DISCOVER_LEADS",
            description=f"Searched synthetic lead repository for industry='{req.target_industry}', region='{req.target_region}'.",
            inputs={"target_industry": req.target_industry, "target_region": req.target_region},
            outputs={"leads_found_count": len(raw_leads), "lead_ids": [l["id"] for l in raw_leads]},
            status="SUCCESS",
            duration_ms=round((t1 - t0) * 1000, 2)
        ))
        step_counter += 1

        # 2. Lead Enrichment Step
        t0 = time.time()
        enriched_leads = []
        for l in raw_leads:
            enriched = self.enrichment_agent.enrich_lead(l)
            enriched_leads.append(enriched)
        t1 = time.time()

        traces.append(AgentStepTrace(
            step=step_counter,
            agent_name="Supervisor -> Lead Enrichment Agent",
            action_type="ENRICH_LEADS",
            description="Analyzed tech stack compatibility, engagement intensity, and decision-maker roles.",
            inputs={"raw_leads_count": len(raw_leads)},
            outputs={"enriched_count": len(enriched_leads)},
            status="SUCCESS",
            duration_ms=round((t1 - t0) * 1000, 2)
        ))
        step_counter += 1

        # 3. Lead Qualification Step
        t0 = time.time()
        qualification_results: List[QualificationResult] = []
        qualified_leads: List[Dict[str, Any]] = []

        for lead_dict in enriched_leads:
            q_res = self.qualification_agent.qualify_lead(lead_dict, req.min_qualification_threshold)
            qualification_results.append(q_res)
            if q_res.status == "QUALIFIED":
                qualified_leads.append(lead_dict)
        t1 = time.time()

        traces.append(AgentStepTrace(
            step=step_counter,
            agent_name="Supervisor -> Lead Qualification Agent",
            action_type="QUALIFY_LEADS",
            description=f"Calculated Fit/Need/Intent/Budget scores against threshold >= {req.min_qualification_threshold}.",
            inputs={"threshold": req.min_qualification_threshold},
            outputs={
                "qualified_count": len(qualified_leads),
                "disqualified_count": len(enriched_leads) - len(qualified_leads)
            },
            status="SUCCESS",
            duration_ms=round((t1 - t0) * 1000, 2)
        ))
        step_counter += 1

        # 4. Email Drafting Step
        t0 = time.time()
        email_drafts: List[EmailDraft] = []
        for q_lead in qualified_leads:
            draft = self.drafting_agent.draft_email(q_lead, req.value_proposition)
            email_drafts.append(draft)
        t1 = time.time()

        traces.append(AgentStepTrace(
            step=step_counter,
            agent_name="Supervisor -> Email Drafting Agent",
            action_type="DRAFT_OUTREACH",
            description=f"Generated personalized cold email previews incorporating value proposition for {len(qualified_leads)} qualified lead(s).",
            inputs={"value_prop": req.value_proposition, "target_leads_count": len(qualified_leads)},
            outputs={"drafts_created_count": len(email_drafts)},
            status="SUCCESS",
            duration_ms=round((t1 - t0) * 1000, 2)
        ))
        step_counter += 1

        # 5. Quality & Compliance Review Step
        t0 = time.time()
        compliance_checks: List[ComplianceCheck] = []
        for idx, q_lead in enumerate(qualified_leads):
            draft = email_drafts[idx]
            check = self.reviewer_agent.review_draft(q_lead, draft)
            compliance_checks.append(check)
        t1 = time.time()

        traces.append(AgentStepTrace(
            step=step_counter,
            agent_name="Supervisor -> Quality & Compliance Reviewer Agent",
            action_type="REVIEW_COMPLIANCE",
            description="Audited email drafts for personalization, claim validity, B2B tone, and compliance standards.",
            inputs={"drafts_reviewed": len(email_drafts)},
            outputs={"approved_count": len([c for c in compliance_checks if c.is_compliant])},
            status="SUCCESS",
            duration_ms=round((t1 - t0) * 1000, 2)
        ))

        total_duration = round((time.time() - start_time) * 1000, 2)

        # Convert lead dicts to Pydantic objects
        lead_objects = [Lead(**l) for l in enriched_leads]

        return SDRWorkflowResponse(
            campaign_industry=req.target_industry,
            leads_discovered_count=len(enriched_leads),
            leads_qualified_count=len(qualified_leads),
            leads=lead_objects,
            qualification_results=qualification_results,
            email_drafts=email_drafts,
            compliance_checks=compliance_checks,
            agent_traces=traces,
            workflow_duration_ms=total_duration
        )
