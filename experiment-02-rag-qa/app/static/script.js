/* ==============================================================================
   Applied Agentic AI Laboratory — UI Interactive Controller
   Experiment 02 — RAG-Based Question Answering System
   ============================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const messagesList = document.getElementById('messages-list');
    const welcomeCard = document.getElementById('welcome-card');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const rebuildIndexBtn = document.getElementById('rebuild-index-btn');
    const providerNameEl = document.getElementById('provider-name');
    const chipBtns = document.querySelectorAll('.chip-btn');

    // Fetch Initial Knowledge Base Status & Health
    fetchHealthAndKBStatus();

    // Event Listener: Form Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = userInput.value.trim();
        if (!question) return;

        userInput.value = '';
        await handleRAGQuery(question);
    });

    // Event Listener: Sample Chips
    chipBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const question = btn.getAttribute('data-question');
            if (question) {
                await handleRAGQuery(question);
            }
        });
    });

    // Event Listener: Rebuild Index
    rebuildIndexBtn.addEventListener('click', async () => {
        rebuildIndexBtn.disabled = true;
        rebuildIndexBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Rebuilding...`;
        try {
            const res = await fetch('/api/index', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ force_rebuild: true })
            });
            if (res.ok) {
                await fetchHealthAndKBStatus();
                alert('✅ Vector index successfully rebuilt from knowledge_base documents!');
            }
        } catch (e) {
            alert('Failed to rebuild index.');
        } finally {
            rebuildIndexBtn.disabled = false;
            rebuildIndexBtn.innerHTML = `<i class="fa-solid fa-rotate"></i> Rebuild Index`;
        }
    });

    // Event Listener: Clear Chat
    clearChatBtn.addEventListener('click', () => {
        messagesList.innerHTML = '';
        if (welcomeCard) welcomeCard.style.display = 'block';
        resetWorkflowBar();
    });

    // Main RAG Pipeline Execution Handler
    async function handleRAGQuery(question) {
        if (welcomeCard) welcomeCard.style.display = 'none';

        appendUserMessage(question);

        // Update Workflow Bar State: Step 1 Active
        updateWorkflowBar([
            { step: 'Document Index', status: 'completed' },
            { step: 'Query Embedding', status: 'in_progress' },
            { step: 'Hybrid Retrieval', status: 'pending' },
            { step: 'Context Building', status: 'pending' },
            { step: 'Response Generation', status: 'pending' },
            { step: 'Grounded Answer', status: 'pending' }
        ]);

        const assistantWrapper = createAssistantPlaceholder();
        messagesList.appendChild(assistantWrapper);
        scrollToBottom();

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, top_k: 4 })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to process RAG query.');
            }

            const data = await response.json();

            if (data.workflow) {
                updateWorkflowBarFromData(data.workflow);
            }

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

    function createAssistantPlaceholder() {
        const wrapper = document.createElement('div');
        wrapper.className = 'message-wrapper assistant';
        wrapper.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-shield-cat"></i></div>
            <div class="message-bubble">
                <div class="loading-state" style="display:flex; align-items:center; gap:0.5rem;">
                    <i class="fa-solid fa-circle-notch fa-spin" style="color: var(--primary);"></i> Executing hybrid retrieval (vector similarity + lexical phrase matching)...
                </div>
            </div>
        `;
        return wrapper;
    }

    function renderAssistantResponse(wrapper, data) {
        const bubble = wrapper.querySelector('.message-bubble');

        if (!data.success) {
            bubble.innerHTML = `
                <div class="out-of-kb-banner">
                    <i class="fa-solid fa-triangle-exclamation"></i> ${escapeHtml(data.explanation || data.error)}
                </div>
            `;
            return;
        }

        const isOut = data.inspector && data.inspector.out_of_scope;

        // Render Answer Text
        let answerHtml = `<div class="explanation-text">${formatMarkdownText(data.answer)}</div>`;

        if (isOut) {
            answerHtml = `
                <div class="out-of-kb-banner">
                    <i class="fa-solid fa-circle-question"></i> ${escapeHtml(data.answer)}
                </div>
            `;
        }

        // Render Retrieved Sources Panel
        let sourcesHtml = '';
        if (data.sources && data.sources.length > 0) {
            const cards = data.sources.map(src => {
                const pctScore = Math.round(src.score * 100);
                const vecScore = src.vector_score !== undefined ? src.vector_score.toFixed(4) : 'N/A';
                const lexScore = src.lexical_score !== undefined ? src.lexical_score.toFixed(4) : 'N/A';
                return `
                    <div class="source-card">
                        <div class="source-card-header">
                            <span class="source-doc-title"><i class="fa-solid fa-file-code"></i> ${escapeHtml(src.document)}</span>
                            <span class="source-score-badge">${pctScore}% Hybrid Match</span>
                        </div>
                        <div class="source-chunk-id">ID: ${escapeHtml(src.chunk_id)} | Vector: ${vecScore} | Lexical: ${lexScore}</div>
                        <div class="source-excerpt">"${escapeHtml(src.excerpt)}"</div>
                    </div>
                `;
            }).join('');

            sourcesHtml = `
                <div class="sources-panel">
                    <div class="sources-panel-title">
                        <i class="fa-solid fa-quote-left"></i> Retrieved Source Evidence (${data.sources.length} Chunks)
                    </div>
                    <div class="sources-grid">
                        ${cards}
                    </div>
                </div>
            `;
        }

        // Render Collapsible RAG Inspector
        let inspectorHtml = '';
        if (data.inspector) {
            const insp = data.inspector;
            inspectorHtml = `
                <details class="inspector-details">
                    <summary class="inspector-summary">
                        <i class="fa-solid fa-microscope"></i> RAG Inspector Diagnostics & Retrieval Metrics
                    </summary>
                    <div class="inspector-body">Query: "${escapeHtml(insp.query)}"
Normalized Query: "${escapeHtml(insp.normalized_query || insp.query)}"
Retrieval Strategy: ${escapeHtml(insp.retrieval_strategy || 'Hybrid (Vector + Lexical)')}
Chunks Searched: ${insp.chunks_searched}
Top-K Requested: ${insp.top_k}
Hybrid Score: ${insp.max_relevance_score}
Vector Similarity Score: ${insp.vector_score !== undefined ? insp.vector_score : 'N/A'}
Lexical Match Score: ${insp.lexical_score !== undefined ? insp.lexical_score : 'N/A'}
Embedding Model: ${insp.embedding_model}
Vector Store: ${insp.vector_store}
Response Mode: ${escapeHtml(insp.response_mode)}
Out of Knowledge Base: ${insp.out_of_scope ? 'YES (Below Threshold)' : 'NO'}</div>
                </details>
            `;
        }

        bubble.innerHTML = `${answerHtml}${sourcesHtml}${inspectorHtml}`;
    }

    function renderAssistantError(wrapper, errorMsg) {
        const bubble = wrapper.querySelector('.message-bubble');
        bubble.innerHTML = `
            <div class="out-of-kb-banner" style="border-color: var(--danger); background: rgba(239, 68, 68, 0.15); color: #fca5a5;">
                <i class="fa-solid fa-circle-xmark"></i> ${escapeHtml(errorMsg)}
            </div>
        `;
    }

    // Knowledge Base Status Fetcher
    async function fetchHealthAndKBStatus() {
        try {
            const hRes = await fetch('/api/health');
            if (hRes.ok) {
                const hData = await hRes.json();
                providerNameEl.textContent = hData.llm_provider || 'MOCK';
            }

            const kbRes = await fetch('/api/knowledge-base/status');
            if (kbRes.ok) {
                const kbData = await kbRes.json();
                document.getElementById('kb-docs-count').textContent = kbData.documents_indexed || 0;
                document.getElementById('kb-chunks-count').textContent = kbData.chunks_indexed || 0;
                document.getElementById('kb-model-name').textContent = kbData.embedding_model || 'local-dense-384';
                document.getElementById('kb-index-type').textContent = kbData.vector_store || 'LocalJSONVectorStore';
                
                if (kbData.last_indexed && kbData.last_indexed !== 'Never') {
                    const d = new Date(kbData.last_indexed);
                    document.getElementById('kb-last-indexed').textContent = d.toLocaleTimeString();
                } else {
                    document.getElementById('kb-last-indexed').textContent = 'Never';
                }
            }
        } catch (e) {
            providerNameEl.textContent = 'MOCK (Offline)';
        }
    }

    // Workflow Bar Controller Functions
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

    function scrollToBottom() {
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
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
