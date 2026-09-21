/**
 * Interactive Client Controller
 * Experiment 04 — SQL Agent with Tool Use (MR23-1CS0436)
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const agentForm = document.getElementById('agent-form');
    const questionInput = document.getElementById('question-input');
    const maxIterationsSelect = document.getElementById('max-iterations');
    const runAgentBtn = document.getElementById('run-agent-btn');
    const clearAllBtn = document.getElementById('clear-all-btn');
    const sampleButtons = document.querySelectorAll('.sample-btn');

    const welcomeCard = document.getElementById('welcome-card');
    const resultsArea = document.getElementById('results-area');
    const finalAnswerText = document.getElementById('final-answer-text');
    const statusBadge = document.getElementById('status-badge');
    const generatedSqlBlock = document.getElementById('generated-sql-block');
    const dataTableContainer = document.getElementById('data-table-container');
    const copySqlBtn = document.getElementById('copy-sql-btn');
    const agentTraceTimeline = document.getElementById('agent-trace-timeline');

    // Tool Metrics DOM Elements
    const countListTables = document.getElementById('count-list-tables');
    const countGetSchema = document.getElementById('count-get-schema');
    const countCheckSyntax = document.getElementById('count-check-syntax');
    const countExecuteSql = document.getElementById('count-execute-sql');
    const countRetries = document.getElementById('count-retries');
    const countTotalCalls = document.getElementById('count-total-calls');

    // Explorer Elements
    const explorerTabs = document.getElementById('explorer-tabs');
    const explorerContent = document.getElementById('explorer-content');

    let currentSchemaData = null;

    // 1. Fetch Health & Schema on Load
    fetchHealth();
    fetchExplorerSchema();

    // Sample Query Clicks
    sampleButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const query = btn.getAttribute('data-query');
            if (query) {
                questionInput.value = query;
                questionInput.focus();
            }
        });
    });

    // Reset Workbench
    clearAllBtn.addEventListener('click', () => {
        questionInput.value = '';
        welcomeCard.style.display = 'block';
        resultsArea.style.display = 'none';
        resetToolCounters();
    });

    // Copy SQL Button
    copySqlBtn.addEventListener('click', () => {
        const sqlText = generatedSqlBlock.textContent;
        if (sqlText) {
            navigator.clipboard.writeText(sqlText);
            copySqlBtn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            setTimeout(() => {
                copySqlBtn.innerHTML = '<i class="fa-solid fa-copy"></i> Copy SQL';
            }, 2000);
        }
    });

    // Form Submit
    agentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = questionInput.value.trim();
        const maxIterations = parseInt(maxIterationsSelect.value, 10) || 8;

        if (!question) return;

        // UI Loading State
        runAgentBtn.disabled = true;
        runAgentBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Executing ReAct Loop...';
        welcomeCard.style.display = 'none';
        resultsArea.style.display = 'block';

        try {
            const res = await fetch('/api/agent/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, max_iterations: maxIterations })
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderAgentResults(data);
        } catch (err) {
            renderErrorState(err.message);
        } finally {
            runAgentBtn.disabled = false;
            runAgentBtn.innerHTML = '<span>Execute ReAct Agent</span> <i class="fa-solid fa-play"></i>';
        }
    });

    async function fetchHealth() {
        try {
            const res = await fetch('/api/health');
            if (res.ok) {
                const data = await res.json();
                document.getElementById('provider-name').textContent = data.llm_provider.toUpperCase();
            }
        } catch (e) {
            console.warn('Health fetch error:', e);
        }
    }

    async function fetchExplorerSchema() {
        try {
            const res = await fetch('/api/database/schema');
            if (res.ok) {
                currentSchemaData = await res.json();
                renderDatabaseExplorer(currentSchemaData);
            }
        } catch (e) {
            console.warn('Explorer fetch error:', e);
        }
    }

    function resetToolCounters() {
        countListTables.textContent = '0';
        countGetSchema.textContent = '0';
        countCheckSyntax.textContent = '0';
        countExecuteSql.textContent = '0';
        countRetries.textContent = '0';
        countTotalCalls.textContent = '0';
    }

    function renderAgentResults(data) {
        // 1. Tool Counters
        if (data.tool_counters) {
            countListTables.textContent = data.tool_counters.list_tables || 0;
            countGetSchema.textContent = data.tool_counters.get_schema || 0;
            countCheckSyntax.textContent = data.tool_counters.check_query_syntax || 0;
            countExecuteSql.textContent = data.tool_counters.execute_sql || 0;
            countRetries.textContent = data.tool_counters.retries || 0;
            countTotalCalls.textContent = data.tool_counters.total_calls || 0;
        }

        // 2. Status Badge & Final Answer
        if (data.success) {
            statusBadge.className = 'badge badge-success';
            statusBadge.textContent = `Completed (${data.iterations_used} Iterations)`;
        } else {
            statusBadge.className = 'badge badge-warning';
            statusBadge.textContent = 'Warning / Incomplete';
        }
        finalAnswerText.innerHTML = formatMarkdownAnswer(data.final_answer);

        // 3. Generated SQL & Data Table
        generatedSqlBlock.textContent = data.generated_sql || 'N/A';
        renderDataTable(data.columns, data.rows);

        // 4. Safe Agent Execution Trace Timeline
        renderAgentTraceTimeline(data.agent_trace || []);
    }

    function renderErrorState(errMsg) {
        statusBadge.className = 'badge badge-danger';
        statusBadge.textContent = 'Failed';
        finalAnswerText.innerHTML = `<p style="color: var(--danger);"><i class="fa-solid fa-triangle-exclamation"></i> Server Error: ${errMsg}</p>`;
        generatedSqlBlock.textContent = 'N/A';
        dataTableContainer.innerHTML = '';
        agentTraceTimeline.innerHTML = '';
    }

    function formatMarkdownAnswer(text) {
        if (!text) return '';
        let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\n/g, '<br>');
        return `<p>${html}</p>`;
    }

    function renderDataTable(columns, rows) {
        if (!columns || columns.length === 0 || !rows || rows.length === 0) {
            dataTableContainer.innerHTML = '<p class="subtitle" style="padding: 0.5rem 0;">No tabular data rows returned.</p>';
            return;
        }

        let html = '<table><thead><tr>';
        columns.forEach(col => {
            html += `<th>${col}</th>`;
        });
        html += '</tr></thead><tbody>';

        rows.forEach(row => {
            html += '<tr>';
            row.forEach(val => {
                const displayVal = (val === null || val === undefined) ? '<em>null</em>' : val;
                html += `<td>${displayVal}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table>';
        dataTableContainer.innerHTML = html;
    }

    function renderAgentTraceTimeline(trace) {
        if (!trace || trace.length === 0) {
            agentTraceTimeline.innerHTML = '<p class="subtitle">No execution steps recorded.</p>';
            return;
        }

        let html = '';
        trace.forEach(item => {
            const statusClass = item.status === 'retry' ? 'status-retry' : (item.status === 'completed' ? 'status-completed' : '');
            
            html += `
                <div class="timeline-item ${statusClass}">
                    <div class="timeline-header">
                        <span class="timeline-step">Step ${item.step}</span>
                        <span class="timeline-tool"><i class="fa-solid fa-wrench"></i> ${item.tool}</span>
                    </div>
                    <div class="timeline-decision">${item.decision_summary}</div>
                    <div class="timeline-observation">
                        <strong>Observation:</strong> ${item.observation}
                    </div>
                </div>
            `;
        });

        agentTraceTimeline.innerHTML = html;
    }

    function renderDatabaseExplorer(data) {
        if (!data || !data.tables) return;

        let tabsHtml = '';
        data.tables.forEach((t, idx) => {
            const activeClass = idx === 0 ? 'active' : '';
            tabsHtml += `<button class="tab-btn ${activeClass}" data-tab="${t.table_name}"><i class="fa-solid fa-table"></i> ${t.table_name} (${t.row_count})</button>`;
        });
        explorerTabs.innerHTML = tabsHtml;

        // Render first table schema by default
        renderExplorerTableContent(data.tables[0]);

        // Tab click listeners
        const tabBtns = explorerTabs.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                const tname = btn.getAttribute('data-tab');
                const targetTable = data.tables.find(t => t.table_name === tname);
                if (targetTable) {
                    renderExplorerTableContent(targetTable);
                }
            });
        });
    }

    function renderExplorerTableContent(table) {
        let html = `
            <div style="margin-bottom: 0.75rem;">
                <strong>Table:</strong> <code>${table.table_name}</code> · <strong>Total Rows:</strong> ${table.row_count}
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Column Name</th>
                        <th>Data Type</th>
                        <th>Primary Key</th>
                    </tr>
                </thead>
                <tbody>
        `;

        table.columns.forEach(c => {
            html += `
                <tr>
                    <td><code>${c.name}</code></td>
                    <td>${c.type}</td>
                    <td>${c.is_primary_key ? '<span class="badge badge-success">PK</span>' : 'No'}</td>
                </tr>
            `;
        });

        html += '</tbody></table>';

        if (table.foreign_keys && table.foreign_keys.length > 0) {
            html += '<div style="margin-top: 0.75rem; font-size: 0.8rem; color: var(--text-muted);"><strong>Foreign Keys:</strong> ';
            const fkStrs = table.foreign_keys.map(fk => `<code>${fk.from_column} → ${fk.to_table}(${fk.to_column})</code>`);
            html += fkStrs.join(', ') + '</div>';
        }

        explorerContent.innerHTML = html;
    }
});
