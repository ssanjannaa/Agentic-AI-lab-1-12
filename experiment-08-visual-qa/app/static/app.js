/**
 * Interactive Client Controller
 * Experiment 08 — Image Retrieval / Visual QA System (MR23-1CS0436)
 */

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchQueryInput = document.getElementById('search-query');
    const categoryFilterSelect = document.getElementById('category-filter');
    const searchBtn = document.getElementById('search-btn');

    const catalogGalleryContainer = document.getElementById('catalog-gallery-container');
    const searchResultsContainer = document.getElementById('search-results-container');

    const selectedImageHeader = document.getElementById('selected-image-header');
    const selectedImageTitle = document.getElementById('selected-image-title');
    const selectedImageDesc = document.getElementById('selected-image-desc');
    const vqaForm = document.getElementById('vqa-form');
    const vqaQuestionInput = document.getElementById('vqa-question');
    const askVqaBtn = document.getElementById('ask-vqa-btn');

    const vqaAnswerContainer = document.getElementById('vqa-answer-container');
    const vqaAnswerBox = document.getElementById('vqa-answer-box');
    const vqaDurationBadge = document.getElementById('vqa-duration-badge');

    let currentSelectedImageId = 'IMG-SOC-01';

    fetchCatalog();

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const query = searchQueryInput.value.trim();
        const category = categoryFilterSelect.value;

        searchBtn.disabled = true;
        searchBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Searching Feature Index...';

        try {
            const res = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query, category_filter: category, top_k: 4 })
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderSearchResults(data.results || []);
        } catch (err) {
            alert(`Search Error: ${err.message}`);
        } finally {
            searchBtn.disabled = false;
            searchBtn.innerHTML = '<span>Search Visual Catalog</span> <i class="fa-solid fa-search"></i>';
        }
    });

    vqaForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const question = vqaQuestionInput.value.trim();
        if (!question) {
            alert('Please enter a question to ask.');
            return;
        }

        askVqaBtn.disabled = true;
        askVqaBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Answering Grounded Question...';
        vqaAnswerContainer.style.display = 'block';

        try {
            const res = await fetch('/api/vqa', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image_id: currentSelectedImageId, question: question })
            });

            if (!res.ok) {
                throw new Error(`HTTP Error: ${res.status}`);
            }

            const data = await res.json();
            renderVQAAnswer(data);
        } catch (err) {
            alert(`Visual QA Error: ${err.message}`);
        } finally {
            askVqaBtn.disabled = false;
            askVqaBtn.innerHTML = '<span>Ask Grounded Visual Question</span> <i class="fa-solid fa-circle-question"></i>';
        }
    });

    async function fetchCatalog() {
        try {
            const res = await fetch('/api/images');
            if (res.ok) {
                const catalog = await res.json();
                renderGallery(catalog);
                if (catalog.length > 0) {
                    selectImage(catalog[0]);
                }
            }
        } catch (e) {
            console.warn('Catalog fetch error:', e);
        }
    }

    function renderGallery(catalog) {
        let html = '';
        catalog.forEach(img => {
            html += `
                <div class="gallery-card ${img.image_id === currentSelectedImageId ? 'selected' : ''}" data-id="${img.image_id}">
                    <div style="font-weight:700; font-size:0.85rem; color:#fff;">${img.title}</div>
                    <div style="font-size:0.75rem; color:var(--text-muted);">${img.category} · ${img.resolution}</div>
                </div>
            `;
        });
        catalogGalleryContainer.innerHTML = html;

        const cards = catalogGalleryContainer.querySelectorAll('.gallery-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                const imgId = card.getAttribute('data-id');
                const targetImg = catalog.find(i => i.image_id === imgId);
                if (targetImg) {
                    cards.forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                    selectImage(targetImg);
                }
            });
        });
    }

    function selectImage(img) {
        currentSelectedImageId = img.image_id;
        selectedImageHeader.style.display = 'block';
        selectedImageTitle.textContent = `${img.title} (${img.image_id})`;
        selectedImageDesc.textContent = `${img.visual_description} · Resolution: ${img.resolution}`;
        vqaForm.style.display = 'block';
    }

    function renderSearchResults(results) {
        if (!results || results.length === 0) {
            searchResultsContainer.innerHTML = '<p class="subtitle">No matching images found.</p>';
            return;
        }

        let html = '';
        results.forEach(r => {
            const img = r.image;
            html += `
                <div class="img-result-card" data-id="${img.image_id}">
                    <div>
                        <div class="img-title">${img.title}</div>
                        <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.4rem;">
                            Category: <strong>${img.category}</strong> (${img.format})
                        </div>
                        <div style="font-size:0.8rem; margin-bottom:0.5rem;">${img.visual_description}</div>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-color); padding-top:0.5rem; margin-top:0.5rem;">
                        <span class="img-score">Similarity: ${r.similarity_score}</span>
                        <button type="button" class="btn btn-secondary select-img-btn" style="padding:0.3rem 0.6rem; font-size:0.75rem;" data-id="${img.image_id}">
                            Select for VQA
                        </button>
                    </div>
                </div>
            `;
        });

        searchResultsContainer.innerHTML = html;

        const selectBtns = searchResultsContainer.querySelectorAll('.select-img-btn');
        selectBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const imgId = btn.getAttribute('data-id');
                fetch('/api/images')
                    .then(r => r.json())
                    .then(catalog => {
                        const target = catalog.find(i => i.image_id === imgId);
                        if (target) selectImage(target);
                    });
            });
        });
    }

    function renderVQAAnswer(data) {
        vqaDurationBadge.style.display = 'inline-block';
        vqaDurationBadge.textContent = `${data.vqa_duration_ms} ms`;

        let html = `
            <div style="font-size:1.05rem; font-weight:700; color:#fff; margin-bottom:0.6rem;">
                <i class="fa-solid fa-comment-dots"></i> Q: ${data.question}
            </div>
            <div style="font-size:0.95rem; color:#67e8f9; margin-bottom:0.8rem; background:rgba(6,182,212,0.1); padding:0.8rem; border-radius:6px; border-left:3px solid var(--primary);">
                <strong>A:</strong> ${data.answer}
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:0.4rem;">
                <strong>Grounded Evidence:</strong> ${(data.grounded_evidence || []).join(' | ')}
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted);">
                <strong>Referenced Catalog Annotations:</strong> ${(data.detected_objects_referenced || []).join(', ')} · <strong>Confidence:</strong> ${data.confidence_score}
            </div>
        `;

        vqaAnswerBox.innerHTML = html;
    }
});
