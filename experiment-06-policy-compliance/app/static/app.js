/**
 * Interactive Client Controller
 * Experiment 06 — Policy Compliance Agent (MR23-1CS0436)
 */

document.addEventListener('DOMContentLoaded', () => {
    const auditForm = document.getElementById('audit-form');
    const policySelect = document.getElementById('policy-select');
    const scenarioTextarea = document.getElementById('scenario-text');
    const runAuditBtn = document.getElementById('run-audit-btn');
    const sampleScenariosContainer = document.getElementById('sample-scenarios-container');

    const welcomeCard = document.getElementById('welcome-card');
    const resultsArea = document.getElementById('results-area');
    const durationBadge = document.getElementById('duration-badge');

    const scoreValEl = document.getElementById('compliance-score-val');
    const overallStatusBadge = document.getElementById('overall-status-badge');
    const rulesTotalVal = document.getElementById('rules-total-val');
    const rulesPassedVal = document.getElementById('rules-passed-val');
    const rulesFailedVal = document.getElementById('rules-failed-val');
    const criticalCountVal = document.getElementById('critical-count-val');

    const ruleEvaluationsContainer = document.getElementById('rule-evaluations-container');
    const remediationsContainer = document.getElementById('remediations-container');

    fetchPolicies();
    fetchScenarios();

    auditForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const policyId = policySelect.value;
        const scenarioText = scenarioTextarea.value.trim();

        if (!scenarioText) {
            alert('Please enter a scenario narrative description to evaluate.');
            return;
        }

        runAuditBtn.disabled = true;
        runAuditBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Running Rule Engine Audit...';
        welcomeCard.style.display = 'none';
        resultsArea.style.display = 'block';

        try {
            const res = await fetch('/api/compliance/audit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ policy_id: policyId, scenario_text: scenarioText })
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderAuditResults(data);
        } catch (err) {
            alert(`Compliance Audit Error: ${err.message}`);
        } finally {
            runAuditBtn.disabled = false;
            runAuditBtn.innerHTML = '<span>Evaluate Policy Compliance</span> <i class="fa-solid fa-magnifying-glass-chart"></i>';
        }
    });

    async function fetchPolicies() {
        try {
            const res = await fetch('/api/policies');
            if (res.ok) {
                const policies = await res.json();
                let html = '';
                policies.forEach(p => {
                    html += `<option value="${p.policy_id}">${p.title} (${p.policy_id})</option>`;
                });
                policySelect.innerHTML = html;
            }
        } catch (e) {
            console.warn('Policies fetch error:', e);
        }
    }

    async function fetchScenarios() {
        try {
            const res = await fetch('/api/scenarios');
            if (res.ok) {
                const scenarios = await res.json();
                let html = '';
                scenarios.forEach(s => {
                    html += `
                        <button type="button" class="sample-btn" data-policy="${s.target_policy_id}" data-desc="${escapeHtml(s.description)}">
                            <i class="fa-solid fa-triangle-exclamation"></i> ${s.title}
                        </button>
                    `;
                });
                sampleScenariosContainer.innerHTML = html;

                // Add click listeners to sample buttons
                const sampleBtns = sampleScenariosContainer.querySelectorAll('.sample-btn');
                sampleBtns.forEach(btn => {
                    btn.addEventListener('click', () => {
                        const targetPolicy = btn.getAttribute('data-policy');
                        const desc = btn.getAttribute('data-desc');
                        policySelect.value = targetPolicy;
                        scenarioTextarea.value = desc;
                        scenarioTextarea.focus();
                    });
                });
            }
        } catch (e) {
            console.warn('Scenarios fetch error:', e);
        }
    }

    function escapeHtml(str) {
        return str.replace(/"/g, '&quot;');
    }

    function renderAuditResults(data) {
        durationBadge.style.display = 'inline-block';
        durationBadge.textContent = `${data.evaluation_duration_ms} ms`;

        scoreValEl.textContent = `${data.compliance_score}%`;
        overallStatusBadge.textContent = data.overall_status;

        if (data.overall_status === 'COMPLIANT') {
            overallStatusBadge.className = 'status-pill status-compliant';
        } else if (data.overall_status === 'WARNING') {
            overallStatusBadge.className = 'status-pill status-warning';
        } else {
            overallStatusBadge.className = 'status-pill status-non-compliant';
        }

        rulesTotalVal.textContent = data.total_rules_evaluated || 0;
        rulesPassedVal.textContent = data.rules_passed || 0;
        rulesFailedVal.textContent = data.rules_failed || 0;
        criticalCountVal.textContent = data.critical_violations_count || 0;

        renderRuleBreakdownTable(data.rule_evaluations || []);
        renderRemediations(data.recommended_remediations || []);
    }

    function renderRuleBreakdownTable(evaluations) {
        if (!evaluations || evaluations.length === 0) {
            ruleEvaluationsContainer.innerHTML = '<p class="subtitle">No rules evaluated.</p>';
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Rule ID</th>
                        <th>Rule Name</th>
                        <th>Severity</th>
                        <th>Status</th>
                        <th>Evaluation Reason</th>
                    </tr>
                </thead>
                <tbody>
        `;

        evaluations.forEach(ev => {
            const badgeClass = ev.status === 'PASS' ? 'badge-pass' : 'badge-fail';
            html += `
                <tr>
                    <td><code>${ev.rule_id}</code></td>
                    <td><strong>${ev.rule_name}</strong></td>
                    <td><span style="font-weight:700; color: ${ev.severity === 'CRITICAL' ? 'var(--danger)' : 'var(--warning)'};">${ev.severity}</span></td>
                    <td><span class="${badgeClass}">${ev.status}</span></td>
                    <td style="font-size: 0.8rem; color: var(--text-muted);">${ev.reason}</td>
                </tr>
            `;
        });

        html += '</tbody></table>';
        ruleEvaluationsContainer.innerHTML = html;
    }

    function renderRemediations(remediations) {
        if (!remediations || remediations.length === 0) {
            remediationsContainer.innerHTML = '<div class="remediation-item" style="background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); color: var(--success);"><i class="fa-solid fa-circle-check"></i> All policy controls verified. No remediation action required.</div>';
            return;
        }

        let html = '';
        remediations.forEach(rem => {
            html += `
                <div class="remediation-item">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <span>${rem}</span>
                </div>
            `;
        });
        remediationsContainer.innerHTML = html;
    }
});
