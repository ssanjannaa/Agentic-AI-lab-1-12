"""
Lead Qualification Agent Tests
Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
"""

from app.services.lead_enrichment_agent import LeadEnrichmentAgent
from app.services.lead_qualification_agent import LeadQualificationAgent
from app.services.lead_discovery_agent import load_all_leads

def test_qualification_scoring_high_fit():
    all_leads = load_all_leads()
    ciso_lead = next(l for l in all_leads if l["id"] == "LEAD-102")
    
    enricher = LeadEnrichmentAgent()
    qualifier = LeadQualificationAgent()

    enriched = enricher.enrich_lead(ciso_lead)
    q_res = qualifier.qualify_lead(enriched, min_threshold=60)

    assert q_res.status == "QUALIFIED"
    assert q_res.final_score >= 80
    assert q_res.fit_score > 0
    assert q_res.need_score > 0

def test_qualification_scoring_low_fit():
    all_leads = load_all_leads()
    unsub_lead = next(l for l in all_leads if l["id"] == "LEAD-106")
    
    enricher = LeadEnrichmentAgent()
    qualifier = LeadQualificationAgent()

    enriched = enricher.enrich_lead(unsub_lead)
    q_res = qualifier.qualify_lead(enriched, min_threshold=60)

    assert q_res.status == "DISQUALIFIED"
    assert q_res.final_score < 60
