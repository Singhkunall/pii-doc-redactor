document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfoBar = document.getElementById('file-info-bar');
    const selectedFilename = document.getElementById('selected-filename');
    const changeFileBtn = document.getElementById('change-file-btn');

    const dashboardSection = document.getElementById('dashboard-section');
    const controlsSection = document.getElementById('controls-section');
    const tableSection = document.getElementById('table-section');
    const previewSection = document.getElementById('preview-section');

    const statTotalCount = document.getElementById('stat-total-count');
    const statNamesCount = document.getElementById('stat-names-count');
    const statContactCount = document.getElementById('stat-contact-count');
    const statLocationCount = document.getElementById('stat-location-count');

    const categoryChipsContainer = document.getElementById('category-chips');
    const saltInput = document.getElementById('salt-input');
    const downloadBtn = document.getElementById('download-btn');
    const tableBody = document.getElementById('entity-table-body');
    const tableEntityCount = document.getElementById('table-entity-count');

    const contentOriginal = document.getElementById('content-original');
    const contentRedacted = document.getElementById('content-redacted');
    const previewContainer = document.getElementById('preview-container');
    const tabBtns = document.querySelectorAll('.tab-btn');

    // State Variables
    let currentFile = null;
    let analysisResult = null;
    let activeCategories = new Set();

    const ALL_CATEGORIES = [
        "EMAIL", "PHONE", "PERSON_NAME", "COMPANY_NAME", 
        "SSN", "CREDIT_CARD", "ADDRESS", "DATE_OF_BIRTH", "IP_ADDRESS"
    ];

    // File Drag and Drop Handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    changeFileBtn.addEventListener('click', () => {
        resetApp();
    });

    saltInput.addEventListener('input', () => {
        if (currentFile) {
            analyzeAndPreview();
        }
    });

    downloadBtn.addEventListener('click', () => {
        downloadRedactedDocx();
    });

    // Preview Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const tab = btn.dataset.tab;
            
            const paneOrig = document.getElementById('pane-original');
            const paneRed = document.getElementById('pane-redacted');

            if (tab === 'split') {
                previewContainer.style.gridTemplateColumns = '1fr 1fr';
                paneOrig.style.display = 'flex';
                paneRed.style.display = 'flex';
            } else if (tab === 'original') {
                previewContainer.style.gridTemplateColumns = '1fr';
                paneOrig.style.display = 'flex';
                paneRed.style.display = 'none';
            } else if (tab === 'redacted') {
                previewContainer.style.gridTemplateColumns = '1fr';
                paneOrig.style.display = 'none';
                paneRed.style.display = 'flex';
            }
        });
    });

    function resetApp() {
        currentFile = null;
        analysisResult = null;
        fileInput.value = '';
        dropZone.parentElement.classList.remove('hidden');
        fileInfoBar.classList.add('hidden');
        dashboardSection.classList.add('hidden');
        controlsSection.classList.add('hidden');
        tableSection.classList.add('hidden');
        previewSection.classList.add('hidden');
    }

    function handleFileSelect(file) {
        currentFile = file;
        selectedFilename.textContent = file.name;
        dropZone.parentElement.classList.add('hidden');
        fileInfoBar.classList.remove('hidden');

        // Reset active categories to include all detected
        activeCategories = new Set(ALL_CATEGORIES);

        analyzeAndPreview();
    }

    async function analyzeAndPreview() {
        if (!currentFile) return;

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('salt', saltInput.value.trim() || 'default');

        try {
            // 1. Run Analysis Endpoint
            const res = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            if (!res.ok) {
                let errMsg = res.statusText || 'Analysis failed';
                try {
                    const err = await res.json();
                    if (err && err.detail) errMsg = err.detail;
                } catch (_) {
                    try {
                        const txt = await res.text();
                        if (txt) errMsg = txt;
                    } catch (_) {}
                }
                alert(`Error analyzing file: ${errMsg}`);
                return;
            }
            analysisResult = await res.json();

            // Render Dashboard & Details
            renderDashboard(analysisResult);
            renderCategoryChips(analysisResult.summary);
            renderEntityTable(analysisResult.details);

            // 2. Fetch Live Preview
            await updatePreview();

            // Show sections
            dashboardSection.classList.remove('hidden');
            controlsSection.classList.remove('hidden');
            tableSection.classList.remove('hidden');
            previewSection.classList.remove('hidden');

        } catch (e) {
            console.error('Failed to analyze file:', e);
            alert('Failed to connect to backend engine.');
        }
    }

    function renderDashboard(data) {
        statTotalCount.textContent = data.total_pii_found;

        const summary = data.summary || {};
        const namesCount = (summary['PERSON_NAME'] || 0) + (summary['COMPANY_NAME'] || 0);
        const contactCount = (summary['EMAIL'] || 0) + (summary['PHONE'] || 0) + (summary['SSN'] || 0) + (summary['CREDIT_CARD'] || 0) + (summary['IP_ADDRESS'] || 0);
        const locationCount = (summary['ADDRESS'] || 0) + (summary['DATE_OF_BIRTH'] || 0);

        statNamesCount.textContent = namesCount;
        statContactCount.textContent = contactCount;
        statLocationCount.textContent = locationCount;
    }

    function renderCategoryChips(summary) {
        categoryChipsContainer.innerHTML = '';
        const detectedCategories = Object.keys(summary);

        if (detectedCategories.length === 0) {
            categoryChipsContainer.innerHTML = '<span style="color: var(--text-dim); font-size: 0.85rem;">No PII categories detected.</span>';
            return;
        }

        detectedCategories.forEach(cat => {
            const chip = document.createElement('div');
            const isActive = activeCategories.has(cat);
            chip.className = `chip ${isActive ? 'active' : 'inactive'}`;
            chip.innerHTML = `
                <span>${cat}</span>
                <span style="opacity: 0.8; font-size: 0.75rem;">(${summary[cat]})</span>
            `;

            chip.addEventListener('click', () => {
                if (activeCategories.has(cat)) {
                    activeCategories.delete(cat);
                } else {
                    activeCategories.add(cat);
                }
                chip.className = `chip ${activeCategories.has(cat) ? 'active' : 'inactive'}`;
                updatePreview();
                filterEntityTable();
            });

            categoryChipsContainer.appendChild(chip);
        });
    }

    function renderEntityTable(details) {
        tableBody.innerHTML = '';
        tableEntityCount.textContent = `${details.length} items`;

        if (details.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 20px;">No PII entities detected in this document.</td></tr>';
            return;
        }

        details.forEach(item => {
            const tr = document.createElement('tr');
            tr.dataset.category = item.category;

            tr.innerHTML = `
                <td>${item.id}</td>
                <td><span class="pii-badge badge-${item.category.toLowerCase()}">${item.category}</span></td>
                <td><code>${escapeHtml(item.original_value)}</code></td>
                <td><code>${escapeHtml(item.fake_value)}</code></td>
                <td style="color: var(--text-dim);">${item.start} : ${item.end}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    function filterEntityTable() {
        const rows = tableBody.querySelectorAll('tr');
        rows.forEach(tr => {
            const cat = tr.dataset.category;
            if (cat) {
                tr.style.display = activeCategories.has(cat) ? '' : 'none';
            }
        });
    }

    async function updatePreview() {
        if (!currentFile) return;

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('salt', saltInput.value.trim() || 'default');
        formData.append('categories', Array.from(activeCategories).join(','));

        try {
            const res = await fetch('/api/preview', {
                method: 'POST',
                body: formData
            });
            if (!res.ok) return;

            const previewData = await res.json();
            contentOriginal.innerHTML = previewData.original_html;
            contentRedacted.innerHTML = previewData.redacted_html;
        } catch (e) {
            console.error('Failed to fetch preview:', e);
        }
    }

    async function downloadRedactedDocx() {
        if (!currentFile) return;

        const fname = currentFile.name.toLowerCase();
        const isDocx = fname.endsWith('.docx');
        const isTxt = fname.endsWith('.txt');

        if (!isDocx && !isTxt) {
            alert('File download is supported for .docx and .txt files.');
            return;
        }

        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('salt', saltInput.value.trim() || 'default');
        formData.append('categories', Array.from(activeCategories).join(','));

        downloadBtn.disabled = true;
        downloadBtn.innerHTML = 'Processing Redaction...';

        try {
            const res = await fetch('/api/redact', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                let errMsg = res.statusText || 'Redaction download failed';
                try {
                    const err = await res.json();
                    if (err && err.detail) errMsg = err.detail;
                } catch (_) {
                    try {
                        const txt = await res.text();
                        if (txt) errMsg = txt;
                    } catch (_) {}
                }
                alert(`Redaction download failed: ${errMsg}`);
                return;
            }

            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Redacted_${currentFile.name}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } catch (e) {
            console.error('Download error:', e);
            alert('Failed to download redacted file.');
        } finally {
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Download Redacted Document
            `;
        }
    }

    function escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
