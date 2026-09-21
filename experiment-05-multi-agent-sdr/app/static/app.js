/**
 * Interactive Client Controller
 * Experiment 05 — Multi-Agent SDR System (MR23-1CS0436)
 */

document.addEventListener('DOMContentLoaded', () => {
    const campaignForm = document.getElementById('campaign-form');
    const targetIndustrySelect = document.getElementById('target-industry');
    const targetRegionSelect = document.getElementById('target-region');
    const qualificationThresholdInput = document.getElementById('qualification-threshold');
    const valuePropTextarea = document.getElementById('value-prop');
    const runCampaignBtn = document.getElementById('run-campaign-btn');

    const welcomeCard = document.getElementById('welcome-card');
    const resultsArea = document.getElementById('results-area');
    const durationBadge = document.getElementById('workflow-duration-badge');

    const discoveredCountEl = document.getElementById('discovered-count');
    const qualifiedCountEl = document.getElementById('qualified-count');
    const draftedCountEl = document.getElementById('drafted-count');
    const approvedCountEl = document.getElementById('approved-count');

    const agentTraceTimeline = document.getElementById('agent-trace-timeline');
    const outreachCardsContainer = document.getElementById('outreach-cards-container');

    fetchHealth();

    campaignForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const reqBody = {
            target_industry: targetIndustrySelect.value,
            target_region: targetRegionSelect.value,
            min_qualification_threshold: parseInt(qualificationThresholdInput.value, 10) || 60,
            value_proposition: valuePropTextarea.value.trim()
        };

        runCampaignBtn.disabled = true;
        runCampaignBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running Multi-Agent Campaign...';
        welcomeCard.style.display = 'none';
        resultsArea.style.display = 'block';

        try {
            const res = await fetch('/api/sdr/campaign', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reqBody)
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderSDRResults(data);
        } catch (err) {
            alert(`SDR Campaign Error: ${err.message}`);
        } finally {
            runCampaignBtn.disabled = false;
            runCampaignBtn.innerHTML = '<span>Launch Multi-Agent SDR Campaign</span> <i class="fa-solid fa-paper-plane"></i>';
        }
    });

    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            if (res.ok) {
                const data = await res.json();
                document.getElementById('provider-name').textContent = `${data.llm_provider.toUpperCase()} Multi-Agent`;
            }
        } catch (e) {
            console.warn('Health fetch error:', e);
        }
    }

    function renderSDRResults(data) {
        durationBadge.style.display = 'inline-block';
        durationBadge.textContent = `${data.workflow_duration_ms} ms`;

        discoveredCountEl.textContent = data.leads_discovered_count || 0;
        qualifiedCountEl.textContent = data.leads_qualified_count || 0;
        draftedCountEl.textContent = data.email_drafts ? data.email_drafts.length : 0;

        const approvedCount = (data.compliance_checks || []).filter(c => c.is_compliant).length;
        approvedCountEl.textContent = approvedCount;

        renderAgentTraces(data.agent_traces || []);
        renderOutreachCards(data);
    }

    function renderAgentTraces(traces) {
        if (!traces || traces.length === 0) {
            agentTraceTimeline.innerHTML = '<p class="subtitle">No agent step traces recorded.</p>';
            return;
        }

        let html = '';
        traces.forEach(t => {
            html += `
                <div class="timeline-item">
                    <div class="timeline-header">
                        <span class="timeline-agent"><i class="fa-solid fa-robot"></i> ${t.agent_name}</span>
                        <span class="timeline-time">${t.duration_ms} ms</span>
                    </div>
                    <div class="timeline-desc"><strong>Action:</strong> ${t.description}</div>
                    <div class="timeline-output">
                        <strong>Outputs:</strong> ${JSON.stringify(t.outputs)}
                    </div>
                </div>
            `;
        });
        agentTraceTimeline.innerHTML = html;
    }

    function renderOutreachCards(data) {
        const leads = data.leads || [];
        const qualResults = data.qualification_results || [];
        const drafts = data.email_drafts || [];
        const checks = data.compliance_checks || [];

        if (leads.length === 0) {
            outreachCardsContainer.innerHTML = '<p class="subtitle">No leads discovered matching the target criteria.</p>';
            return;
        }

        let html = '';
        leads.forEach(lead => {
            const qRes = qualResults.find(q => q.lead_id === lead.id);
            const draft = drafts.find(d => d.lead_id === lead.id);
            const check = checks.find(c => c.lead_id === lead.id);

            const isQualified = qRes && qRes.status === 'QUALIFIED';
            const badgeClass = isQualified ? 'badge-qualified' : 'badge-disqualified';

            html += `
                <div class="lead-outreach-card">
                    <div class="lead-card-header">
                        <div class="lead-name-title">
                            <h4>${lead.contact_name} · ${lead.contact_role}</h4>
                            <p class="subtitle">${lead.company_name} (${lead.industry}) — ${lead.region}</p>
                        </div>
                        <div class="score-badge-group">
                            <span class="score-badge ${badgeClass}">
                                ${qRes ? qRes.final_score : 0}/100 — ${qRes ? qRes.status : 'N/A'}
                            </span>
                        </div>
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">
                        <strong>Business Need:</strong> ${lead.business_need}<br>
                        <strong>Engagement Signals:</strong> ${(lead.engagement_signals || []).join(', ')}
                    </div>
            `;

            if (isQualified && draft) {
                html += `
                    <div class="email-preview-box">
                        <div class="email-subject"><i class="fa-solid fa-envelope"></i> <strong>Subject:</strong> ${draft.subject_line}</div>
                        <div class="email-body-text">${draft.email_body}</div>
                    </div>
                `;

                if (check) {
                    html += `
                        <div class="compliance-box">
                            <i class="fa-solid fa-shield-halved"></i> <strong>Compliance Reviewer Verdict:</strong> ${check.review_verdict} · ${check.compliance_notes.join(' | ')}
                        </div>
                    `;
                }
            } else {
                html += `
                    <div style="font-size: 0.825rem; color: var(--warning); padding: 0.5rem 0;">
                        <i class="fa-solid fa-ban"></i> Disqualified for outbound campaign. Qualification summary: ${qRes ? qRes.qualification_summary : 'Did not meet score threshold.'}
                    </div>
                `;
            }

            html += '</div>';
        });

        outreachCardsContainer.innerHTML = html;
    }
});
