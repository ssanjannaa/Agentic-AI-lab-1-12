/**
 * Interactive Client Controller
 * Experiment 09 — Reasoning Model Benchmarking (MR23-1CS0436)
 */

document.addEventListener('DOMContentLoaded', () => {
    const benchmarkForm = document.getElementById('benchmark-form');
    const taskSelect = document.getElementById('task-select');
    const customProblemTextarea = document.getElementById('custom-problem');
    const runBenchmarkBtn = document.getElementById('run-benchmark-btn');

    const durationBadge = document.getElementById('benchmark-duration-badge');
    const winnersBanner = document.getElementById('winners-banner');
    const winnerAccuracyVal = document.getElementById('winner-accuracy-val');
    const winnerEfficiencyVal = document.getElementById('winner-efficiency-val');

    const strategiesContainer = document.getElementById('strategies-container');
    const tradeoffContainer = document.getElementById('tradeoff-container');
    const tradeoffText = document.getElementById('tradeoff-text');

    let benchmarkTasks = [];

    fetchTasks();

    taskSelect.addEventListener('change', () => {
        const selectedId = taskSelect.value;
        const targetTask = benchmarkTasks.find(t => t.task_id === selectedId);
        if (targetTask) {
            customProblemTextarea.value = targetTask.problem_statement;
        }
    });

    benchmarkForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const reqBody = {
            task_id: taskSelect.value,
            custom_problem_statement: customProblemTextarea.value.trim()
        };

        runBenchmarkBtn.disabled = true;
        runBenchmarkBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Executing Benchmark...';

        try {
            const res = await fetch('/api/benchmark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reqBody)
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderBenchmarkResults(data);
        } catch (err) {
            console.error('Benchmark error:', err);
            alert(`Benchmark Execution Failed: ${err.message}`);
        } finally {
            runBenchmarkBtn.disabled = false;
            runBenchmarkBtn.innerHTML = '<span>Execute Strategy Benchmark</span> <i class="fa-solid fa-gauge-high"></i>';
        }
    });

    async function fetchTasks() {
        try {
            const res = await fetch('/api/tasks');
            if (res.ok) {
                benchmarkTasks = await res.json();
                taskSelect.innerHTML = '';
                benchmarkTasks.forEach(t => {
                    const opt = document.createElement('option');
                    opt.value = t.task_id;
                    opt.textContent = `${t.task_id} — ${t.title} (${t.complexity})`;
                    taskSelect.appendChild(opt);
                });
                if (benchmarkTasks.length > 0) {
                    customProblemTextarea.value = benchmarkTasks[0].problem_statement;
                }
            }
        } catch (e) {
            console.warn('Task fetch error:', e);
        }
    }

    function renderBenchmarkResults(data) {
        if (durationBadge) {
            durationBadge.style.display = 'inline-block';
            durationBadge.textContent = `${data.benchmark_duration_ms} ms`;
        }

        if (winnersBanner) winnersBanner.style.display = 'grid';
        if (winnerAccuracyVal) winnerAccuracyVal.textContent = data.winning_strategy_accuracy;
        if (winnerEfficiencyVal) winnerEfficiencyVal.textContent = data.winning_strategy_efficiency;

        renderStrategyCards(data.strategy_results || []);

        if (tradeoffContainer) tradeoffContainer.style.display = 'block';
        if (tradeoffText) tradeoffText.textContent = data.tradeoff_synthesis || 'No synthesis recorded.';
    }

    function renderStrategyCards(results) {
        if (!strategiesContainer) return;

        if (!results || results.length === 0) {
            strategiesContainer.innerHTML = '<p class="subtitle">No strategy evaluation results.</p>';
            return;
        }

        let html = '';
        results.forEach(res => {
            const m = res.metrics;
            const steps = res.reasoning_steps || res.observable_execution_steps || [];
            html += `
                <div class="strategy-card">
                    <div>
                        <div class="strategy-header">
                            <i class="fa-solid fa-cube"></i> ${res.strategy_name}
                        </div>
                        <div style="font-size:0.85rem; margin-bottom:0.6rem; color:var(--text-main);">
                            ${res.output_summary}
                        </div>
                        <div style="font-size:0.8rem; background:rgba(0,0,0,0.3); padding:0.5rem; border-radius:6px; margin-bottom:0.75rem;">
                            <strong>Observable Execution Steps:</strong>
                            <ul style="padding-left:1.2rem; margin-top:0.3rem;">
                                ${steps.map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.4rem; font-size:0.75rem; border-top:1px solid var(--border-color); padding-top:0.6rem; font-family:var(--font-mono);">
                        <div>Correctness: <strong style="color:var(--success);">${m.correctness_score}/100</strong></div>
                        <div>Rigor: <strong style="color:var(--secondary);">${m.logical_rigor_score}/100</strong></div>
                        <div>Latency: <strong>${m.latency_ms} ms</strong></div>
                        <div>Tokens: <strong>${m.estimated_tokens}</strong></div>
                    </div>
                </div>
            `;
        });
        strategiesContainer.innerHTML = html;
    }
});
