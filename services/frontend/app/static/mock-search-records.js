/**
 * Mock Search Records Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    let MOCK_RECORDS = [];
    let currentResults = [];

    // Formatter
    const formatDateTime = (isoString) => {
        const d = new Date(isoString);
        return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    };

    const getStatusClass = (status) => {
        if (status === 'Approved') return 'status-chip-success';
        if (status === 'Escalated') return 'status-chip-danger';
        if (status === 'Rejected') return 'status-chip-danger'; // or maybe neutral, but keeping it visible
        if (status === 'Archived') return 'status-chip-warning'; // using warning for grey/neutral
        return 'status-chip-warning';
    };

    const isMobile = () => window.innerWidth <= 768;

    // Toast Utility
    const showToast = (message) => {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerText = message;
        container.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    };

    // 2. Render Results
    const renderTable = () => {
        const tbody = document.getElementById('searchResultsBody');
        const emptyState = document.getElementById('searchEmptyState');
        const resultsCount = document.getElementById('resultsCount');
        const badge = document.getElementById('totalRecordsBadge');

        resultsCount.innerText = `Showing ${currentResults.length} records`;
        badge.innerText = `${currentResults.length} Records`;

        if (currentResults.length === 0) {
            tbody.innerHTML = '';
            document.getElementById('searchTable').style.display = isMobile() ? 'none' : 'table';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';
        document.getElementById('searchTable').style.display = isMobile() ? 'block' : 'table';

        if (isMobile()) {
            // Render as cards
            tbody.innerHTML = currentResults.map(r => `
                <tr class="queue-card-mobile" data-id="${r.id}">
                    <td>
                        <div class="card-header">
                            <span class="card-id">${r.id}</span>
                            <span class="status-chip ${getStatusClass(r.status)}">${r.status}</span>
                        </div>
                        <div class="card-title">${r.plate}</div>
                        <div class="card-meta">
                            <span>${r.type}</span> • <span>${r.cam}</span>
                        </div>
                        <div class="card-footer">
                            <span class="card-time">${formatDateTime(r.time)}</span>
                            <span class="card-score">${r.score}% Conf</span>
                        </div>
                    </td>
                </tr>
            `).join('');
        } else {
            // Render as table rows
            tbody.innerHTML = currentResults.map(r => `
                <tr class="queue-row" data-id="${r.id}">
                    <td class="font-medium">${r.id}</td>
                    <td class="font-bold">${r.plate}</td>
                    <td>${r.type}</td>
                    <td class="truncate" style="max-width: 150px;">${r.cam}</td>
                    <td class="text-muted" style="font-size: 0.8125rem;">${formatDateTime(r.time)}</td>
                    <td><span class="score-badge ${r.score > 89 ? 'score-high' : (r.score > 74 ? 'score-med' : 'score-low')}">${r.score}%</span></td>
                    <td><span class="status-chip ${getStatusClass(r.status)}">${r.status}</span></td>
                    <td>${r.reviewer}</td>
                    <td class="col-actions">
                        <button class="btn btn-secondary btn-sm" onclick="event.stopPropagation(); window.location.href='./case-detail.html?id=${r.id}'">View</button>
                    </td>
                </tr>
            `).join('');
        }

        // Attach Row Clicks
        document.querySelectorAll('.queue-row, .queue-card-mobile').forEach(row => {
            row.addEventListener('click', () => {
                window.location.href = `/static/case-detail.html?id=${row.dataset.id}`;
            });
        });
    };

    // 3. Search and Filter Logic
    const inputs = {
        search: document.getElementById('globalSearchInput'),
        type: document.getElementById('filterType'),
        status: document.getElementById('filterStatus'),
        cam: document.getElementById('filterCam'),
        reviewer: document.getElementById('filterReviewer'),
        date: document.getElementById('filterDateRange'),
        conf: document.getElementById('filterConf'),
        sort: document.getElementById('sortResults'),
        saved: document.getElementById('savedSearchSelect')
    };

    const activeFiltersList = document.getElementById('activeFiltersList');

    const updateActiveFilterChips = () => {
        let chipsHTML = '';
        
        if (inputs.search.value.trim() !== '') {
            chipsHTML += `<div class="filter-chip-active">Search: ${inputs.search.value}</div>`;
        }
        if (inputs.type.value !== '') {
            chipsHTML += `<div class="filter-chip-active">Type: ${inputs.type.options[inputs.type.selectedIndex].text}</div>`;
        }
        if (inputs.status.value !== '') {
            chipsHTML += `<div class="filter-chip-active">Status: ${inputs.status.value}</div>`;
        }
        if (inputs.cam.value !== '') {
            chipsHTML += `<div class="filter-chip-active">Cam: ${inputs.cam.value}</div>`;
        }
        if (inputs.reviewer.value !== '') {
            chipsHTML += `<div class="filter-chip-active">Rev: ${inputs.reviewer.value}</div>`;
        }
        if (inputs.date.value !== '') {
            chipsHTML += `<div class="filter-chip-active">Date: ${inputs.date.options[inputs.date.selectedIndex].text}</div>`;
        }
        if (inputs.conf.value !== '') {
            chipsHTML += `<div class="filter-chip-active">Conf: ${inputs.conf.options[inputs.conf.selectedIndex].text}</div>`;
        }

        activeFiltersList.innerHTML = chipsHTML;
    };

    const applyFilters = () => {
        const term = inputs.search.value.toLowerCase().trim();
        const type = inputs.type.value;
        const status = inputs.status.value;
        const cam = inputs.cam.value;
        const rev = inputs.reviewer.value;
        const date = inputs.date.value;
        const conf = inputs.conf.value;

        currentResults = MOCK_RECORDS.filter(r => {
            // Text Search
            if (term && !r.id.toLowerCase().includes(term) && !r.plate.toLowerCase().includes(term) && !r.cam.toLowerCase().includes(term)) return false;
            
            // Dropdowns
            if (type && r.type !== type) return false;
            if (status && r.status !== status) return false;
            if (cam && r.cam !== cam) return false;
            if (rev && r.reviewer !== rev) return false;

            // Confidence
            if (conf === 'high' && r.score < 90) return false;
            if (conf === 'med' && (r.score < 75 || r.score > 89)) return false;
            if (conf === 'low' && r.score >= 75) return false;

            // Date (mock logic based on creation time logic)
            // Since mock dates are spread over last 500 hours (~20 days), we can mock this:
            const rDate = new Date(r.time);
            const now = new Date();
            const diffHours = (now - rDate) / (1000 * 60 * 60);
            
            if (date === 'today' && diffHours > 24) return false;
            if (date === 'last7' && diffHours > 24*7) return false;
            if (date === 'last30' && diffHours > 24*30) return false;

            return true;
        });

        applySort();
        updateActiveFilterChips();
        renderTable();
    };

    const applySort = () => {
        const sortMode = inputs.sort.value;
        currentResults.sort((a, b) => {
            if (sortMode === 'newest') return new Date(b.time) - new Date(a.time);
            if (sortMode === 'oldest') return new Date(a.time) - new Date(b.time);
            if (sortMode === 'highest_conf') return b.score - a.score;
            if (sortMode === 'lowest_conf') return a.score - b.score;
            return 0;
        });
    };

    // Event Listeners for Filters
    document.getElementById('btnSearch').addEventListener('click', applyFilters);
    inputs.search.addEventListener('keyup', (e) => { if(e.key === 'Enter') applyFilters(); });
    
    [inputs.type, inputs.status, inputs.cam, inputs.reviewer, inputs.date, inputs.conf].forEach(sel => {
        sel.addEventListener('change', () => {
            inputs.saved.value = ""; // Reset saved search if user manually tweaks
            applyFilters();
        });
    });

    inputs.sort.addEventListener('change', () => {
        applySort();
        renderTable();
    });

    const clearFilters = () => {
        inputs.search.value = '';
        inputs.type.value = '';
        inputs.status.value = '';
        inputs.cam.value = '';
        inputs.reviewer.value = '';
        inputs.date.value = '';
        inputs.conf.value = '';
        inputs.saved.value = '';
        applyFilters();
    };

    document.getElementById('btnClearFilters').addEventListener('click', clearFilters);
    document.getElementById('btnEmptyClear').addEventListener('click', clearFilters);

    // Saved Search Logic
    inputs.saved.addEventListener('change', (e) => {
        clearFilters(); // reset first
        const val = e.target.value;
        if (val === 'helmet_7days') {
            inputs.type.value = 'Helmet Non-Compliance';
            inputs.date.value = 'last7';
        } else if (val === 'escalated_redlight') {
            inputs.type.value = 'Red-Light Violation';
            inputs.status.value = 'Escalated';
        } else if (val === 'low_confidence') {
            inputs.conf.value = 'low';
        } else if (val === 'cam_a12_parking') {
            inputs.cam.value = 'CAM-East-05';
            inputs.type.value = 'Illegal Parking';
        }
        
        // Restore dropdown value since clearFilters erased it
        inputs.saved.value = val;
        applyFilters();
    });

    // Actions
    document.getElementById('btnSaveSearch').addEventListener('click', () => {
        showToast('Current filter combination saved successfully.');
    });

    document.getElementById('btnExport').addEventListener('click', () => {
        if (currentResults.length === 0) {
            showToast('No records to export.');
            return;
        }
        showToast(`Exporting ${currentResults.length} records to CSV...`);
    });

    // Handle Window Resize for Table <-> Cards
    let wasMobile = isMobile();
    window.addEventListener('resize', () => {
        const currentlyMobile = isMobile();
        if (wasMobile !== currentlyMobile) {
            wasMobile = currentlyMobile;
            renderTable();
        }
    });

    // Boot
    const boot = async () => {
        try {
            const apiData = await ApiClient.getQueue(); // Fetch up to limit
            MOCK_RECORDS = apiData.map(c => ({
                id: c.id,
                plate: c.plate || "Unknown",
                type: c.type,
                cam: c.cam,
                time: c.time,
                score: c.score,
                status: c.status,
                reviewer: c.assignee
            }));
            currentResults = [...MOCK_RECORDS];
            applyFilters();
        } catch (e) {
            console.error("Failed to fetch records", e);
        }
    };
    boot();
});
