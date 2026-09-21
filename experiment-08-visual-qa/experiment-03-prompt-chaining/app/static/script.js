/* ==============================================================================
   Applied Agentic AI Laboratory — UI Interactive Controller
   Experiment 03 — Prompt Chaining for Summarization
   ============================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const summarizeForm = document.getElementById('summarize-form');
    const documentInput = document.getElementById('document-input');
    const styleSelect = document.getElementById('summary-style');
    const lengthSelect = document.getElementById('summary-length');
    const summarizeBtn = document.getElementById('summarize-btn');
    const clearAllBtn = document.getElementById('clear-all-btn');
    const sampleBtns = document.querySelectorAll('.sample-btn');

    const welcomeCard = document.getElementById('welcome-card');
    const resultsArea = document.getElementById('results-area');

    // Fetch initial modes & health
    fetchHealthAndModes();

    // Event Listener: Sample Buttons Click
    sampleBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const sampleId = btn.getAttribute('data-sample');
            try {
                const res = await fetch(`/api/samples?id=${sampleId}`);
                if (res.ok) {
                    const sampleData = await res.json();
                    documentInput.value = sampleData.content;
                }
            } catch (e) {
                console.error("Failed to load sample", e);
            }
        });
    });

    // Event Listener: Form Submit
    summarizeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = documentInput.value.trim();
        if (!text) {
            alert('Please paste document text or load a sample document.');
            return;
        }

        const style = styleSelect.value;
        const length = lengthSelect.value;

        await executePromptChainRequest(text, style, length);
    });

    // Event Listener: Clear Studio Workspace
    clearAllBtn.addEventListener('click', () => {
        documentInput.value = '';
        if (welcomeCard) welcomeCard.style.display = 'block';
        if (resultsArea) resultsArea.style.display = 'none';
        resetWorkflowBar();
    });

    // Main API Execution Handler
    async function executePromptChainRequest(text, style, length) {
        summarizeBtn.disabled = true;
        summarizeBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Executing Chain...`;

        if (welcomeCard) welcomeCard.style.display = 'none';

        // Step 1 Active
        updateWorkflowBar([
            { step: 'Document Analysis', status: 'in_progress' },
            { step: 'Key Extraction', status: 'pending' },
            { step: 'Draft Summary', status: 'pending' },
            { step: 'Critique', status: 'pending' },
            { step: 'Refinement', status: 'pending' },
            { step: 'Final Output', status: 'pending' }
        ]);

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    summary_style: style,
                    summary_length: length
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Prompt chaining execution failed.');
            }

            const data = await response.json();

            // Mark all 6 steps completed
            updateWorkflowBar([
                { step: 'Document Analysis', status: 'completed' },
                { step: 'Key Extraction', status: 'completed' },
                { step: 'Draft Summary', status: 'completed' },
                { step: 'Critique', status: 'completed' },
                { step: 'Refinement', status: 'completed' },
                { step: 'Final Output', status: 'completed' }
            ]);

            renderResults(data, style);

        } catch (error) {
            alert(`Error: ${error.message}`);
            updateWorkflowBarError();
        } finally {
            summarizeBtn.disabled = false;
            summarizeBtn.innerHTML = `<span>Execute Prompt Chain</span> <i class="fa-solid fa-play"></i>`;
        }
    }

    function renderResults(data, style) {
        if (resultsArea) resultsArea.style.display = 'flex';

        // Render Metrics
        if (data.metrics) {
            document.getElementById('metric-orig-words').textContent = data.metrics.original_word_count || 0;
            document.getElementById('metric-final-words').textContent = data.metrics.final_word_count || 0;
            document.getElementById('metric-ratio').textContent = data.metrics.compression_ratio || '0%';
            document.getElementById('metric-key-points').textContent = data.metrics.key_points_extracted || 0;
            document.getElementById('metric-time').textContent = `${data.metrics.total_processing_time_ms || 0} ms`;
        }

        // Render Final Summary
        document.getElementById('final-style-badge').textContent = style.toUpperCase();
        document.getElementById('final-summary-text').innerHTML = formatMarkdownText(data.final_summary);

        // Render Side-by-Side Comparison: Draft vs Refined Summary
        document.getElementById('draft-summary-text').textContent = data.draft_summary || 'N/A';
        document.getElementById('refined-summary-comparison-text').textContent = data.final_summary || 'N/A';

        // Render Key Points
        const keyPointsList = document.getElementById('key-points-list');
        keyPointsList.innerHTML = '';
        if (data.key_points && data.key_points.length > 0) {
            data.key_points.forEach(kp => {
                const li = document.createElement('li');
                li.textContent = kp;
                keyPointsList.appendChild(li);
            });
        } else {
            keyPointsList.innerHTML = '<li>No specific key points extracted.</li>';
        }

        // Render Terms Glossary
        const termsList = document.getElementById('terms-list');
        termsList.innerHTML = '';
        if (data.important_terms && data.important_terms.length > 0) {
            data.important_terms.forEach(t => {
                const card = document.createElement('div');
                card.className = 'term-card';
                card.innerHTML = `<span class="term-title">${escapeHtml(t.term)}:</span> ${escapeHtml(t.definition)}`;
                termsList.appendChild(card);
            });
        } else {
            termsList.innerHTML = '<div class="term-card">No specialized terms extracted.</div>';
        }

        // Render Prompt Chain Inspector Accordion
        const inspectorBody = document.getElementById('inspector-body');
        inspectorBody.innerHTML = '';

        if (data.chain_trace && data.chain_trace.length > 0) {
            data.chain_trace.forEach(stg => {
                const card = document.createElement('div');
                card.className = 'stage-inspect-card';
                card.innerHTML = `
                    <div class="stage-inspect-header">
                        <span>Stage ${stg.stage}: ${escapeHtml(stg.name)}</span>
                        <span>${stg.execution_time_ms} ms</span>
                    </div>
                    <div class="stage-inspect-inputs">
                        <strong>Purpose:</strong> ${escapeHtml(stg.purpose)}<br>
                        <strong>Inputs Consumed:</strong> ${stg.inputs_consumed.join(', ')}
                    </div>
                    <div class="stage-inspect-preview">${escapeHtml(stg.output_preview)}</div>
                `;
                inspectorBody.appendChild(card);
            });
        }
    }

    async function fetchHealthAndModes() {
        try {
            const res = await fetch('/api/health');
            if (res.ok) {
                const h = await res.json();
                document.getElementById('provider-name').textContent = h.llm_provider || 'Offline Mode';
            }
        } catch (e) {
            console.error("Health check error", e);
        }
    }

    function updateWorkflowBar(steps) {
        steps.forEach((stepItem, index) => {
            const stepEl = document.getElementById(`step-${index}`);
            if (stepEl) {
                stepEl.className = 'step-chip';
                if (stepItem.status === 'completed') stepEl.classList.add('completed');
                else if (stepItem.status === 'in_progress') stepEl.classList.add('active');
                else if (stepItem.status === 'failed') stepEl.classList.add('failed');
            }
        });
    }

    function updateWorkflowBarError() {
        for (let i = 0; i < 6; i++) {
            const stepEl = document.getElementById(`step-${i}`);
            if (stepEl && !stepEl.classList.contains('completed')) {
                stepEl.className = 'step-chip failed';
                break;
            }
        }
    }

    function resetWorkflowBar() {
        for (let i = 0; i < 6; i++) {
            const stepEl = document.getElementById(`step-${i}`);
            if (stepEl) stepEl.className = 'step-chip';
        }
    }

    function formatMarkdownText(str) {
        if (typeof str !== 'string') return str;
        let formatted = escapeHtml(str);
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        formatted = formatted.replace(/\n\n/g, '<br><br>');
        return formatted;
    }

    function escapeHtml(str) {
        if (typeof str !== 'string') return str;
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
