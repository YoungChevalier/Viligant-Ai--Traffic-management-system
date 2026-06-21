/**
 * Mock Dashboard Logic
 */

document.addEventListener('DOMContentLoaded', async () => {
    
    // Load Dashboard Summary
    try {
        const summary = await ApiClient.getDashboardSummary();
        const kpis = summary.kpis;
        document.querySelector('.kpi-card:nth-child(1) .kpi-val').innerText = kpis.pending_review;
        document.querySelector('.kpi-card:nth-child(2) .kpi-val').innerText = kpis.total_cases;
        document.querySelector('.kpi-card:nth-child(3) .kpi-val').innerText = kpis.escalated;
        document.querySelector('.kpi-card:nth-child(4) .kpi-val').innerText = kpis.active_alerts;
    } catch (e) {
        console.error("Failed to load KPIs", e);
    }

    // Load recent detections
    try {
        const cases = await ApiClient.getQueue({ limit: 10 });
        renderDetections(cases.slice(0, 8)); // Show top 8
    } catch (e) {
        console.error("Failed to load recent cases", e);
        renderDetections([]);
    }

    // Load Alerts
    try {
        const alerts = await ApiClient.getAlerts();
        renderAlerts(alerts.slice(0, 4)); // Show top 4
    } catch (e) {
        console.error("Failed to load alerts", e);
        renderAlerts([]);
    }

    const getStatusClass = (status) => {
        if (status === 'Approved') return 'status-chip-success';
        if (status === 'Escalated') return 'status-chip-danger';
        return 'status-chip-warning';
    };

    const getSevClass = (sev) => {
        if (sev === 'critical') return 'alert-critical';
        if (sev === 'warning') return 'alert-warning';
        return 'alert-info';
    };

    const renderDetections = (detections) => {
        const body = document.getElementById('detectionsListBody');
        const empty = document.getElementById('detectionsEmptyState');
        
        if (detections.length === 0) {
            body.innerHTML = '';
            empty.style.display = 'block';
            return;
        }

        empty.style.display = 'none';
        body.innerHTML = detections.map(d => `
            <div class="detection-row">
                <div class="col-id"><a href="#">${d.id}</a></div>
                <div class="col-type truncate">${d.type}</div>
                <div class="col-plate"><strong>${d.plate}</strong></div>
                <div class="col-cam truncate">${d.cam}</div>
                <div class="col-time">${new Date(d.time).toLocaleTimeString()}</div>
                <div class="col-score">${d.score}%</div>
                <div class="col-status"><span class="status-chip ${getStatusClass(d.status)}">${d.status}</span></div>
            </div>
        `).join('');
    };

    const renderAlerts = (alerts) => {
        const body = document.getElementById('systemAlertsBody');
        const empty = document.getElementById('alertsEmptyState');

        if (alerts.length === 0) {
            body.innerHTML = '';
            empty.style.display = 'block';
            return;
        }

        empty.style.display = 'none';
        body.innerHTML = alerts.map(a => `
            <div class="alert-item ${getSevClass(a.sev)}">
                <div class="alert-header">
                    <span class="alert-title">${a.title}</span>
                    <span class="alert-time">${a.time}</span>
                </div>
                <div class="alert-desc">${a.description}</div>
            </div>
        `).join('');
    };

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
        
        // trigger animation
        requestAnimationFrame(() => toast.classList.add('show'));

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    };

    // Export Button
    document.getElementById('exportBtn').addEventListener('click', () => {
        showToast("Report export started. Preparing data...");
    });

    document.getElementById('generateSummaryBtn').addEventListener('click', () => {
        showToast("Generating Daily Summary report...");
    });

    // Refresh Data
    document.getElementById('refreshBtn').addEventListener('click', () => {
        const grid = document.getElementById('dashboardGridContainer');
        grid.classList.add('dashboard-loading');
        
        showToast("Refreshing dashboard data...");

        setTimeout(() => {
            grid.classList.remove('dashboard-loading');
            
            // Randomize KPI values
            document.getElementById('kpiTotal').innerText = (1492 + Math.floor(Math.random() * 50)).toLocaleString();
            document.getElementById('kpiPending').innerText = (345 + Math.floor(Math.random() * 20 - 10)).toLocaleString();
            
            // Shuffle detections slightly
            const newDetections = [...MOCK_DETECTIONS];
            const first = newDetections.shift();
            newDetections.push(first);
            renderDetections(newDetections);
            
            showToast("Dashboard data is up to date.");
        }, 800);
    });

    // Notification Mock Logic
    const markReadBtn = document.querySelector('.btn-mark-read');
    const filterChips = document.querySelectorAll('.filter-chip');
    const notifItems = document.querySelectorAll('.notification-item');
    const notifEmpty = document.querySelector('.notification-empty');
    const notifLinks = document.querySelectorAll('.notification-menu .btn-link');
    const notifIndicator = document.querySelector('.notification-indicator');

    const updateEmptyState = () => {
        const anyVisible = Array.from(notifItems).some(item => item.style.display !== 'none');
        if (notifEmpty) {
            notifEmpty.style.display = anyVisible ? 'none' : 'block';
        }
    };

    if (markReadBtn) {
        markReadBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // prevent dropdown close if click bubbles
            notifItems.forEach(item => {
                item.classList.remove('unread');
                const dot = item.querySelector('.unread-dot');
                if (dot) dot.style.display = 'none';
            });
            if (notifIndicator) notifIndicator.style.display = 'none';
            showToast("All notifications marked as read.");
        });
    }

    if (filterChips) {
        filterChips.forEach(chip => {
            chip.addEventListener('click', (e) => {
                e.stopPropagation(); // prevent dropdown close
                // Remove active class from all
                filterChips.forEach(c => c.classList.remove('active'));
                const target = e.currentTarget;
                target.classList.add('active');
                
                const filterText = target.innerText.toLowerCase();
                
                notifItems.forEach(item => {
                    if (filterText === 'all') {
                        item.style.display = 'flex';
                    } else {
                        if (item.classList.contains(`category-${filterText}`)) {
                            item.style.display = 'flex';
                        } else {
                            item.style.display = 'none';
                        }
                    }
                });
                
                updateEmptyState();
            });
        });
    }

    if (notifLinks) {
        notifLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.stopPropagation(); // prevent dropdown close
                showToast(`Action triggered: ${e.target.innerText}`);
            });
        });
    }

    // Quick Actions
    const quickDashboardBtn = document.getElementById('quickDashboardBtn');
    const quickClockBtn = document.getElementById('quickClockBtn');

    if (quickDashboardBtn) {
        quickDashboardBtn.addEventListener('click', () => {
            showToast('Layout options opened.');
        });
    }

    if (quickClockBtn) {
        quickClockBtn.addEventListener('click', () => {
            showToast('Recent activity log opened.');
        });
    }

});
