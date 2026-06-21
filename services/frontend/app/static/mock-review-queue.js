/**
 * Mock Review Queue Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    let MOCK_DATA = [];
    let currentData = [];
    let selectedIds = new Set();
    let currentTab = "All";

    // 2. DOM Elements
    const searchInput = document.getElementById('filterSearch');
    const filterType = document.getElementById('filterType');
    const filterCamera = document.getElementById('filterCamera');
    const filterSort = document.getElementById('filterSort');
    const clearFiltersBtn = document.getElementById('clearFiltersBtn');
    
    const tabs = document.querySelectorAll('.tab-item');
    
    const tableBody = document.getElementById('queueTableBody');
    const mobileBody = document.getElementById('queueMobileBody');
    const emptyState = document.getElementById('queueEmptyState');
    const loadingState = document.getElementById('queueLoadingState');
    
    const selectAllCb = document.getElementById('selectAllCb');
    const bulkActionBar = document.getElementById('bulkActionBar');
    const bulkCountDisplay = document.getElementById('bulkCountDisplay');
    const queueMainArea = document.getElementById('queueMainArea');

    // Counts
    const updateCounts = () => {
        const counts = { All: 0, Pending: 0, Flagged: 0, Escalated: 0, Reviewed: 0 };
        MOCK_DATA.forEach(d => {
            counts.All++;
            if (counts[d.status] !== undefined) counts[d.status]++;
        });
        
        document.getElementById('countAll').innerText = counts.All;
        document.getElementById('countPending').innerText = counts.Pending;
        document.getElementById('countFlagged').innerText = counts.Flagged;
        document.getElementById('countEscalated').innerText = counts.Escalated;
        document.getElementById('countReviewed').innerText = counts.Reviewed;

        const pendingCount = counts.Pending + counts.Flagged;
        document.getElementById('headerQueueBadge').innerText = `${pendingCount} Pending`;
        document.getElementById('navQueueBadge').innerText = pendingCount;
    };

    // 3. Render Logic
    const formatTime = (isoString) => {
        const date = new Date(isoString);
        return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    };

    const getStatusClass = (status) => {
        if (status === 'Reviewed') return 'status-chip-success';
        if (status === 'Escalated' || status === 'Flagged') return 'status-chip-danger';
        return 'status-chip-warning';
    };

    const render = () => {
        if (currentData.length === 0) {
            tableBody.innerHTML = '';
            mobileBody.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';

        // Desktop
        tableBody.innerHTML = currentData.map(d => `
            <div class="queue-row" data-id="${d.id}">
                <div class="col-check" onclick="event.stopPropagation()">
                    <input type="checkbox" class="form-checkbox row-checkbox" value="${d.id}" ${selectedIds.has(d.id) ? 'checked' : ''}>
                </div>
                <div class="col-thumb">
                    <div class="thumb-placeholder">${d.thumb}</div>
                </div>
                <div class="col-id font-medium">${d.id}</div>
                <div class="col-type truncate" title="${d.type}">${d.type}</div>
                <div class="col-plate font-semibold">${d.plate}</div>
                <div class="col-cam truncate">${d.cam}</div>
                <div class="col-time text-muted">${formatTime(d.time)}</div>
                <div class="col-score">
                    <span class="${d.score > 90 ? 'text-success' : 'text-warning'} font-medium">${d.score}%</span>
                </div>
                <div class="col-status">
                    <span class="status-chip ${getStatusClass(d.status)}">${d.status}</span>
                </div>
                <div class="col-assign text-muted truncate">${d.assignee}</div>
                <div class="col-actions text-right" onclick="event.stopPropagation()">
                    <div class="action-menu-compact">
                        <button class="btn-icon btn-sm action-approve" title="Approve" data-id="${d.id}">✓</button>
                        <button class="btn-icon btn-sm action-reject" title="Reject" data-id="${d.id}">✕</button>
                        <button class="btn-icon btn-sm action-more" title="More" data-id="${d.id}">⋮</button>
                    </div>
                </div>
            </div>
        `).join('');

        // Mobile
        mobileBody.innerHTML = currentData.map(d => `
            <div class="queue-card-mobile" data-id="${d.id}">
                <div class="card-mobile-header">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <input type="checkbox" class="form-checkbox row-checkbox" value="${d.id}" ${selectedIds.has(d.id) ? 'checked' : ''} onclick="event.stopPropagation()">
                        <span class="font-medium">${d.id}</span>
                    </div>
                    <span class="status-chip ${getStatusClass(d.status)}">${d.status}</span>
                </div>
                <div class="card-mobile-body">
                    <div class="thumb-placeholder" style="width: 48px; height: 48px; font-size: 1.5rem;">${d.thumb}</div>
                    <div class="card-mobile-info">
                        <div class="font-semibold">${d.plate}</div>
                        <div class="text-muted text-sm">${d.type}</div>
                        <div class="text-muted text-sm">${d.cam} • ${formatTime(d.time)}</div>
                    </div>
                    <div class="card-mobile-score">
                        <span class="${d.score > 90 ? 'text-success' : 'text-warning'} font-medium">${d.score}%</span>
                    </div>
                </div>
                <div class="card-mobile-actions" onclick="event.stopPropagation()">
                    <button class="btn btn-secondary btn-sm flex-1 action-reject" data-id="${d.id}">Reject</button>
                    <button class="btn btn-primary btn-sm flex-1 action-approve" data-id="${d.id}">Approve</button>
                </div>
            </div>
        `).join('');

        attachRowListeners();
        updateBulkBar();
    };

    // 4. Filtering and Sorting
    const applyFilters = () => {
        queueMainArea.classList.add('dashboard-loading');

        setTimeout(() => {
            const query = searchInput.value.toLowerCase();
            const type = filterType.value;
            const cam = filterCamera.value;
            const sort = filterSort.value;

            currentData = MOCK_DATA.filter(d => {
                // Tab filter
                if (currentTab !== "All" && d.status !== currentTab) return false;
                
                // Search filter
                if (query && !d.id.toLowerCase().includes(query) && !d.plate.toLowerCase().includes(query)) return false;

                // Dropdowns
                if (type && d.type !== type) return false;
                if (cam && d.cam !== cam) return false;

                return true;
            });

            // Sorting
            currentData.sort((a, b) => {
                if (sort === 'time-desc') return new Date(b.time) - new Date(a.time);
                if (sort === 'time-asc') return new Date(a.time) - new Date(b.time);
                if (sort === 'conf-desc') return b.score - a.score;
                if (sort === 'conf-asc') return a.score - b.score;
                return 0;
            });

            // Clean up selections that are no longer in view
            const visibleIds = new Set(currentData.map(d => d.id));
            for (let id of selectedIds) {
                if (!visibleIds.has(id)) selectedIds.delete(id);
            }
            selectAllCb.checked = currentData.length > 0 && selectedIds.size === currentData.length;

            render();
            queueMainArea.classList.remove('dashboard-loading');
        }, 300); // Simulate processing
    };

    // 5. Event Listeners
    searchInput.addEventListener('input', applyFilters);
    filterType.addEventListener('change', applyFilters);
    filterCamera.addEventListener('change', applyFilters);
    filterSort.addEventListener('change', applyFilters);

    clearFiltersBtn.addEventListener('click', () => {
        searchInput.value = '';
        filterType.value = '';
        filterCamera.value = '';
        filterSort.value = 'time-desc';
        applyFilters();
    });

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            tabs.forEach(t => t.classList.remove('active'));
            const target = e.currentTarget;
            target.classList.add('active');
            currentTab = target.dataset.tab;
            applyFilters();
        });
    });

    selectAllCb.addEventListener('change', (e) => {
        if (e.target.checked) {
            currentData.forEach(d => selectedIds.add(d.id));
        } else {
            selectedIds.clear();
        }
        render();
    });

    // 6. Interaction Logic
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

    const attachRowListeners = () => {
        // Row check boxes
        document.querySelectorAll('.row-checkbox').forEach(cb => {
            cb.addEventListener('change', (e) => {
                if (e.target.checked) {
                    selectedIds.add(e.target.value);
                } else {
                    selectedIds.delete(e.target.value);
                }
                
                selectAllCb.checked = currentData.length > 0 && selectedIds.size === currentData.length;
                updateBulkBar();
                
                // Keep checkboxes synced between mobile/desktop views visually
                document.querySelectorAll(`.row-checkbox[value="${e.target.value}"]`).forEach(el => el.checked = e.target.checked);
            });
        });

        // Row clicks (navigate to case detail)
        document.querySelectorAll('.queue-row, .queue-card-mobile').forEach(row => {
            row.addEventListener('click', () => {
                window.location.href = `/static/case-detail.html?id=${row.dataset.id}`;
            });
        });

        // Action Buttons
        document.querySelectorAll('.action-approve').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                updateItemStatus(btn.dataset.id, 'Reviewed', 'Approve');
            });
        });

        document.querySelectorAll('.action-reject').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                updateItemStatus(btn.dataset.id, 'Reviewed', 'Reject');
            });
        });

        document.querySelectorAll('.action-more').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                showToast(`More actions for ${btn.dataset.id}...`);
            });
        });
    };

    const updateItemStatus = async (id, newStatus, actionName) => {
        try {
            await ApiClient.submitDecision(id, actionName);
            const item = MOCK_DATA.find(d => d.id === id);
            if (item) {
                item.status = newStatus;
                showToast(`${actionName} action successful on ${id}`);
                updateCounts();
                applyFilters();
            }
        } catch (e) {
            showToast(`Failed to ${actionName} case ${id}`);
            console.error(e);
        }
    };

    // Bulk Actions
    const updateBulkBar = () => {
        if (selectedIds.size > 0) {
            bulkCountDisplay.innerText = `${selectedIds.size} selected`;
            bulkActionBar.classList.add('visible');
        } else {
            bulkActionBar.classList.remove('visible');
        }
    };

    document.getElementById('bulkAssignBtn').addEventListener('click', () => {
        showToast(`Assigned ${selectedIds.size} cases to yourself.`);
        selectedIds.clear();
        applyFilters();
    });

    document.getElementById('bulkEscalateBtn').addEventListener('click', () => {
        selectedIds.forEach(id => {
            const item = MOCK_DATA.find(d => d.id === id);
            if (item) item.status = 'Escalated';
        });
        showToast(`Escalated ${selectedIds.size} cases.`);
        selectedIds.clear();
        updateCounts();
        applyFilters();
    });

    document.getElementById('bulkReviewedBtn').addEventListener('click', () => {
        selectedIds.forEach(id => {
            const item = MOCK_DATA.find(d => d.id === id);
            if (item) item.status = 'Reviewed';
        });
        showToast(`Marked ${selectedIds.size} cases as reviewed.`);
        selectedIds.clear();
        updateCounts();
        applyFilters();
    });

    // Boot
    const boot = async () => {
        queueMainArea.classList.add('dashboard-loading');
        try {
            MOCK_DATA = await ApiClient.getQueue();
            currentData = [...MOCK_DATA];
            updateCounts();
            applyFilters();
        } catch (e) {
            console.error(e);
            showToast("Failed to load queue");
        } finally {
            queueMainArea.classList.remove('dashboard-loading');
        }
    };
    boot();
});
