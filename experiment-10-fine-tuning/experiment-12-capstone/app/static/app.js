/**
 * Frontend Interactive Logic for Agentic Cyber Defense Command Center
 * Experiment 12 — Agentic Cybersecurity Research & Incident Decision Assistant (MR23-1CS0436)
 */

document.addEventListener("DOMContentLoaded", () => {
    const sampleSelect = document.getElementById("sampleIncidentSelect");
    const queryInput = document.getElementById("queryInput");
    const analyzeBtn = document.getElementById("analyzeBtn");

    // Pre-populate input when sample incident selected
    sampleSelect.addEventListener("change", async (e) => {
        const incId = e.target.value;
        if (!incId) return;

        try {
            const res = await fetch("/api/incidents");
            const incidents = await res.json();
            const selected = incidents.find(i => i.id === incId);
            if (selected) {
                queryInput.value = `[${selected.id}] ${selected.title}: ${selected.description}`;
            }
        } catch (err) {
            console.error("Failed to load sample incidents:", err);
        }
    });

    // Analyze Incident Button Click
    analyzeBtn.addEventListener("click", async () => {
        const queryText = queryInput.value.trim();
        const selectedIncId = sampleSelect.value;

        if (!queryText && !selectedIncId) {
            alert("Please enter a query or select a sample incident.");
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = "<span>⏳ Executing Multi-Agent Pipeline...</span>";

        resetUIState();

        try {
            const payload = {
                query: queryText || "Analyze incident activity",
                incident_id: selectedIncId || null,
                max_reflection_cycles: 1
            };

            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Server returned HTTP ${response.status}`);
            }

            const data = await response.json();
            renderOrchestrationResults(data);

        } catch (error) {
            console.error("Analysis Error:", error);
            alert("Analysis failed: " + error.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = "<span>🚀 Analyze Incident & Execute Agents</span>";
        }
    });

    function resetUIState() {
        document.getElementById("intentCategoryBadge").textContent = "Processing...";
        document.getElementById("intentCategoryBadge").className = "badge secondary";
        document.getElementById("traceIdBadge").textContent = "Trace: Executing...";

        // Reset agent status badges
        document.querySelectorAll(".agent-status-badge").forEach(badge => {
            badge.textContent = "Running...";
            badge.className = "agent-status-badge pending";
        });
    }

    function renderOrchestrationResults(data) {
        // 1. Intent & Trace
        document.getElementById("intentCategoryBadge").textContent = data.intent_category;
        document.getElementById("intentCategoryBadge").className = "badge supported";
        document.getElementById("traceIdBadge").textContent = `Trace: ${data.trace_id}`;

        // 2. Supervisor Plan
        const planList = document.getElementById("supervisorPlanList");
        planList.innerHTML = "";
        data.workflow_plan.forEach(step => {
            const li = document.createElement("li");
            li.className = "plan-item";
            li.textContent = step;
            planList.appendChild(li);
        });

        // 3. Agent Pipeline Badges
        data.agent_trace.forEach(trace => {
            const card = document.getElementById(`agent-${trace.agent_name}`);
            if (card) {
                const badge = card.querySelector(".agent-status-badge");
                if (badge) {
                    badge.textContent = trace.status;
                    badge.className = `agent-status-badge ${trace.status.toLowerCase()}`;
                }
            }
        });

        // 4. RAG Evidence
        const evContainer = document.getElementById("evidenceContainer");
        evContainer.innerHTML = "";
        if (data.retrieved_evidence.length === 0) {
            evContainer.innerHTML = "<p class='text-muted'>No direct evidence chunks retrieved.</p>";
        } else {
            data.retrieved_evidence.forEach(ev => {
                const div = document.createElement("div");
                div.className = "evidence-box";
                div.innerHTML = `
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <strong>📄 ${ev.document_name}</strong>
                        <span class="badge secondary">Score: ${ev.relevance_score}</span>
                    </div>
                    <div style="color:var(--text-muted); font-size:11px;">${ev.content}</div>
                `;
                evContainer.appendChild(div);
            });
        }

        // 5. Tool Logs
        const toolContainer = document.getElementById("toolLogsContainer");
        toolContainer.innerHTML = "";
        data.tool_calls.forEach(tl => {
            const div = document.createElement("div");
            div.className = "tool-box";
            div.innerHTML = `
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <strong>🔧 ${tl.tool_name}</strong>
                    <span style="color:var(--accent-teal); font-size:11px;">${tl.duration_ms} ms</span>
                </div>
                <pre style="font-family:var(--font-mono); font-size:10px; color:var(--accent-blue); overflow-x:auto;">${JSON.stringify(tl.output_result, null, 2)}</pre>
            `;
            toolContainer.appendChild(div);
        });

        // 6. Security Assessment & MITRE
        const saContainer = document.getElementById("securityAssessmentContainer");
        const sa = data.security_assessment;
        let mitreHtml = sa.mitre_attack_mappings.map(m => `<span class="mitre-pill">${m.id}: ${m.name}</span>`).join("");
        saContainer.innerHTML = `
            <div style="margin-bottom:8px;">
                <strong>Category:</strong> ${sa.incident_category} | <strong>Severity:</strong> <span class="badge ${sa.severity.toLowerCase()}">${sa.severity}</span>
            </div>
            <div style="margin-bottom:8px;">
                <strong>MITRE Techniques:</strong><br>${mitreHtml || "None mapped"}
            </div>
            <div>
                <strong>Technical Findings:</strong>
                <ul style="padding-left:18px; margin-top:4px;">
                    ${sa.technical_findings.map(f => `<li>${f}</li>`).join("")}
                </ul>
            </div>
        `;

        // 7. Compliance Audit
        const caContainer = document.getElementById("complianceAuditContainer");
        const ca = data.compliance_audit;
        const ref = data.reflection_result;
        caContainer.innerHTML = `
            <div style="margin-bottom:8px;">
                <strong>Grounding Status:</strong> <span class="badge supported">${ca.grounding_status}</span>
            </div>
            <div style="margin-bottom:8px;">
                <strong>Defensive Safety Rules Verified:</strong> <span style="color:var(--accent-green)">${ca.is_defensive_compliant ? "✅ PASSED (Strictly Defensive)" : "⚠️ WARNING"}</span>
            </div>
            <div style="margin-bottom:8px;">
                <strong>Critic Review Pass:</strong> ${ref.critic_passed ? "✅ Passed" : "⚠️ Review Flagged"}
            </div>
            <div style="font-size:11px; color:var(--text-muted);">
                ${ca.audit_notes}
            </div>
        `;

        // 8. Final Report
        const reportContainer = document.getElementById("finalReportContainer");
        const rpt = data.final_report;
        reportContainer.innerHTML = `
            <div style="margin-bottom:12px; font-size:13px; color:var(--text-main);">
                <strong>Executive Summary:</strong><br>${rpt.executive_summary}
            </div>
            <div style="margin-bottom:12px;">
                <strong>Recommended Defensive Actions:</strong>
                <ol style="padding-left:20px; margin-top:4px;">
                    ${rpt.recommended_defensive_actions.map(act => `<li style="margin-bottom:4px;">${act}</li>`).join("")}
                </ol>
            </div>
            <div style="font-size:11px; color:var(--text-muted);">
                <strong>Verified Sources:</strong> ${rpt.sources.join(", ")}
            </div>
        `;

        // 9. Metrics Footer
        const m = data.execution_metrics;
        document.getElementById("mRuntime").textContent = `${m.total_execution_time_ms} ms`;
        document.getElementById("mAgents").textContent = m.agents_executed_count;
        document.getElementById("mTools").textContent = m.tools_called_count;
        document.getElementById("mEvidence").textContent = m.evidence_chunks_retrieved;
        document.getElementById("mGrounding").textContent = m.compliance_grounding_status;
    }
});
