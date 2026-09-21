/**
 * Interactive Client Controller
 * Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
 */

document.addEventListener('DOMContentLoaded', () => {
    const optForm = document.getElementById('opt-form');
    const baseModelSelect = document.getElementById('base-model');
    const targetHardwareSelect = document.getElementById('target-hardware');
    const runOptBtn = document.getElementById('run-opt-btn');

    const welcomeCard = document.getElementById('welcome-card');
    const resultsArea = document.getElementById('results-area');
    const durationBadge = document.getElementById('opt-duration-badge');

    const vramChampionVal = document.getElementById('vram-champion-val');
    const throughputChampionVal = document.getElementById('throughput-champion-val');

    const profilesCardsContainer = document.getElementById('profiles-cards-container');
    const synthesisBox = document.getElementById('synthesis-box');

    optForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const reqBody = {
            base_model_name: baseModelSelect.value,
            target_hardware: targetHardwareSelect.value
        };

        runOptBtn.disabled = true;
        runOptBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Executing Benchmark...';

        try {
            const res = await fetch('/api/optimization/benchmark', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reqBody)
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderOptimizationResults(data);
        } catch (err) {
            console.error('Optimization error:', err);
            alert(`Optimization Benchmark Error: ${err.message}`);
        } finally {
            runOptBtn.disabled = false;
            runOptBtn.innerHTML = '<span>Execute Optimization Benchmark</span> <i class="fa-solid fa-bolt"></i>';
        }
    });

    function renderOptimizationResults(data) {
        if (welcomeCard) welcomeCard.style.display = 'none';
        if (resultsArea) resultsArea.style.display = 'block';

        if (durationBadge) {
            durationBadge.style.display = 'inline-block';
            durationBadge.textContent = `${data.evaluation_duration_ms} ms`;
        }

        if (vramChampionVal) vramChampionVal.textContent = data.file_size_reduction_champion || data.vram_reduction_champion;
        if (throughputChampionVal) throughputChampionVal.textContent = data.throughput_champion;

        renderProfilesCards(data.profiles || []);

        if (synthesisBox) synthesisBox.textContent = data.optimization_synthesis || 'No synthesis recorded.';
    }

    function renderProfilesCards(profiles) {
        if (!profilesCardsContainer) return;

        if (!profiles || profiles.length === 0) {
            profilesCardsContainer.innerHTML = '<p class="subtitle">No profiles evaluated.</p>';
            return;
        }

        let html = '';
        profiles.forEach(p => {
            const m = p.metrics;
            let perfText = '';
            if (m.forward_passes_sec && m.forward_passes_sec > 0) {
                perfText = `<div>Forward Throughput: <strong style="color:var(--success);">${m.forward_passes_sec} passes/s</strong></div>`;
            } else if (m.synthetic_operations_sec && m.synthetic_operations_sec > 0) {
                perfText = `<div>Microbenchmark: <strong style="color:var(--text-muted);">${m.synthetic_operations_sec} ops/s</strong></div>`;
            } else {
                perfText = `<div>Throughput: <strong>N/A</strong></div>`;
            }

            html += `
                <div class="profile-card" style="background:var(--card-bg); border:1px solid var(--border-color); border-radius:12px; padding:1rem; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:var(--text-main); margin-bottom:0.4rem; display:flex; align-items:center; gap:0.5rem;">
                            <i class="fa-solid fa-compress" style="color:var(--primary);"></i> ${p.level_name}
                        </div>
                        <div style="font-size:0.85rem; font-weight:600; color:var(--primary); margin-bottom:0.4rem;">
                            ${p.technique}
                        </div>
                        <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.6rem;">
                            ${p.description}
                        </div>
                        <div style="font-size:0.75rem; background:rgba(0,0,0,0.3); padding:0.4rem; border-radius:6px; margin-bottom:0.6rem; word-break:break-all; font-family:var(--font-mono);">
                            <strong>Disk Artifact:</strong> ${p.artifact_path || 'Serialized Matrix'}
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.4rem; font-size:0.75rem; border-top:1px solid var(--border-color); padding-top:0.6rem; font-family:var(--font-mono);">
                        <div>Disk Size: <strong>${m.serialized_file_size_mb} MB</strong></div>
                        <div>Size Reduction: <strong style="color:var(--success);">${m.compression_ratio_percent}%</strong></div>
                        <div>Measured Latency: <strong>${m.measured_latency_ms} ms</strong></div>
                        ${perfText}
                        <div style="grid-column: span 2;">Reconstruction Error (MSE): <strong style="color:var(--secondary);">${m.reconstruction_mse}</strong></div>
                    </div>
                </div>
            `;
        });
        profilesCardsContainer.innerHTML = html;
    }
});
