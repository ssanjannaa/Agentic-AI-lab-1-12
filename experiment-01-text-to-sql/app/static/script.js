/* ==============================================================================
   Applied Agentic AI Laboratory — UI Interactive Controller
   Experiment 01 — Text-to-SQL Workflow
   ============================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const messagesList = document.getElementById('messages-list');
    const welcomeCard = document.getElementById('welcome-card');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const providerNameEl = document.getElementById('provider-name');
    const chipBtns = document.querySelectorAll('.chip-btn');

    // Fetch API Health & Loaded Provider Status
    fetchHealthStatus();

    // Event Listener: Form Submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInput.value.trim();
        if (!question) return;

        userInput.value = '';
        await handleUserQuery(question);
    });

    // Event Listener: Example Chips Click
    chipBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const question = btn.getAttribute('data-question');
            if (question) {
                await handleUserQuery(question);
            }
        });
    });

    // Event Listener: Clear Chat
    clearChatBtn.addEventListener('click', () => {
        messagesList.innerHTML = '';
        welcomeCard.style.display = 'block';
        resetWorkflowBar();
    });

    // Main Query Execution Handler
    async function handleUserQuery(question) {
        // Hide welcome card on first message
        if (welcomeCard) {
            welcomeCard.style.display = 'none';
        }

        // Append User Message Bubble
        appendUserMessage(question);

        // Update Workflow Bar State: Step 1 Active
        updateWorkflowBar([
            { step: 'Question', status: 'completed' },
            { step: 'Schema Retrieval', status: 'in_progress' },
            { step: 'SQL Generation', status: 'pending' },
            { step: 'Safety Validation', status: 'pending' },
            { step: 'DB Execution', status: 'pending' },
            { step: 'Explanation', status: 'pending' }
        ]);

        // Create Assistant Placeholder Message Bubble
        const assistantWrapper = createAssistantMessagePlaceholder();
        messagesList.appendChild(assistantWrapper);
        scrollToBottom();

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to communicate with Text-to-SQL backend.');
            }

            const data = await response.json();

            // Update Workflow Bar based on API response
            if (data.workflow) {
                updateWorkflowBarFromData(data.workflow);
            }

            // Render Full Response Card
            renderAssistantResponse(assistantWrapper, data);

        } catch (error) {
            updateWorkflowBarError();
            renderAssistantError(assistantWrapper, error.message);
        } finally {
            scrollToBottom();
        }
    }

    function appendUserMessage(text) {
        const wrapper = document.createElement('div');
        wrapper.className = 'message-wrapper user';
        wrapper.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-user"></i></div>
            <div class="message-bubble">${escapeHtml(text)}</div>
        `;
        messagesList.appendChild(wrapper);
        scrollToBottom();
    }

    function createAssistantMessagePlaceholder() {
        const wrapper = document.createElement('div');
        wrapper.className = 'message-wrapper assistant';
        wrapper.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-bubble">
                <div class="loading-state">
                    <i class="fa-solid fa-circle-notch fa-spin"></i> Processing Text-to-SQL workflow...
                </div>
            </div>
        `;
        return wrapper;
    }

    function renderAssistantResponse(wrapper, data) {
        const bubble = wrapper.querySelector('.message-bubble');

        if (!data.success) {
            bubble.innerHTML = `
                <div class="error-banner">
                    <i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.explanation || data.error)}
                </div>
            `;
            return;
        }

        // Format Table HTML
        let tableHtml = '';
        if (data.rows && data.rows.length > 0) {
            const headers = data.columns.map(c => `<th>${escapeHtml(c)}</th>`).join('');
            const bodyRows = data.rows.map(row => {
                const cells = row.map(cell => `<td>${escapeHtml(cell !== null ? String(cell) : 'NULL')}</td>`).join('');
                return `<tr>${cells}</tr>`;
            }).join('');

            tableHtml = `
                <div class="table-wrapper">
                    <table class="result-table">
                        <thead><tr>${headers}</tr></thead>
                        <tbody>${bodyRows}</tbody>
                    </table>
                </div>
            `;
        } else {
            tableHtml = `<div class="info-note" style="color: var(--text-muted); font-size: 0.85rem; margin-top: 0.5rem;"><i class="fa-solid fa-info-circle"></i> Query executed successfully but returned 0 rows.</div>`;
        }

        bubble.innerHTML = `
            <div class="explanation-text">${escapeHtml(data.explanation)}</div>
            
            <div class="query-meta-box">
                <div class="meta-header">
                    <span><i class="fa-solid fa-code"></i> Generated SQL Query</span>
                    <span><i class="fa-solid fa-table"></i> Tables: ${data.tables_used.join(', ')}</span>
                </div>
                <div class="sql-code-block">${escapeHtml(data.generated_sql)}</div>
            </div>

            ${tableHtml}
        `;
    }

    function renderAssistantError(wrapper, errorMsg) {
        const bubble = wrapper.querySelector('.message-bubble');
        bubble.innerHTML = `
            <div class="error-banner">
                <i class="fa-solid fa-circle-xmark"></i> ${escapeHtml(errorMsg)}
            </div>
        `;
    }

    // Workflow Bar State Controllers
    function updateWorkflowBarFromData(workflow) {
        workflow.forEach((stepItem, index) => {
            const stepEl = document.getElementById(`step-${index}`);
            if (stepEl) {
                stepEl.className = 'step-chip';
                if (stepItem.status === 'completed') stepEl.classList.add('completed');
                else if (stepItem.status === 'in_progress') stepEl.classList.add('active');
                else if (stepItem.status === 'failed') stepEl.classList.add('failed');
            }
        });
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

    async function fetchHealthStatus() {
        try {
            const res = await fetch('/api/health');
            if (res.ok) {
                const data = await res.json();
                providerNameEl.textContent = data.llm_provider || 'MOCK';
            }
        } catch (e) {
            providerNameEl.textContent = 'MOCK (Offline)';
        }
    }

    function scrollToBottom() {
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
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
