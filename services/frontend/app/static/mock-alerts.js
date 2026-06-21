/**
 * Mock Alerts Center Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    const MOCK_ALERTS = [
        { id: "ALT-042", title: "Camera Offline - Connection Lost", severity: "Critical", source: "Camera", timestamp: "Just now", status: "Unread", entity: "CAM-N-01", desc: "The camera endpoint has lost connection to the main processing server. No heartbeat received for the last 5 minutes.", action: "Check network connectivity on the local switch. Dispatch a field technician if connection cannot be reestablished remotely." },
        { id: "ALT-041", title: "OCR Confidence Drop Spike", severity: "Warning", source: "OCR", timestamp: "10 mins ago", status: "Unread", entity: "System-Wide", desc: "Average plate detection confidence dropped below 60% across 5 nodes. Potentially due to extreme weather or lighting conditions.", action: "Verify local weather conditions. Review raw feeds for CAM-E-04 and CAM-E-05 to manually verify visibility." },
        { id: "ALT-040", title: "Reviewer Queue Overloaded", severity: "Warning", source: "Queue", timestamp: "25 mins ago", status: "Open", entity: "R. Vargas (REV-1042)", desc: "Reviewer assigned queue exceeds 80 pending cases, increasing average turnaround time to >2 minutes.", action: "Reassign 20 cases to available reviewers or mark reviewer as Busy." },
        { id: "ALT-039", title: "System Sync Delayed", severity: "Info", source: "System", timestamp: "1 hour ago", status: "Acknowledged", entity: "Database Node 2", desc: "Data synchronization between core DB and analytics warehouse is lagging by 45 seconds.", action: "Monitor the queue. If lag exceeds 120 seconds, investigate indexing performance." },
        { id: "ALT-038", title: "Feed Degraded (High Packet Loss)", severity: "Warning", source: "Camera", timestamp: "2 hours ago", status: "Unread", entity: "CAM-S-02", desc: "RTSP feed packet loss exceeded 5%. Frames are dropping, impacting violation tracking accuracy.", action: "Switch feed to lower resolution fallback. Check switch bandwidth saturation." },
        { id: "ALT-037", title: "Escalation Volume Increased", severity: "Info", source: "Reviewer", timestamp: "3 hours ago", status: "Resolved", entity: "A. Smith (REV-1089)", desc: "Reviewer escalation rate exceeded 15% in the last hour.", action: "Supervisor reviewed escalated cases. False alarms due to dirt on plates. Resolved." },
        { id: "ALT-036", title: "Repeated ANPR Failure", severity: "Critical", source: "OCR", timestamp: "5 hours ago", status: "Resolved", entity: "CAM-W-11", desc: "Zero plates successfully extracted over the last 50 vehicle passes.", action: "Camera lens was obscured by debris. Field team dispatched and cleaned. Feed restored." },
        { id: "ALT-035", title: "Queue Backlog Warning", severity: "Critical", source: "Queue", timestamp: "1 day ago", status: "Resolved", entity: "Global Queue", desc: "Unassigned cases exceeded 500 items. Review SLA breached.", action: "Called in additional reviewers to clear the backlog. System load balanced." }
    ];

    const getSeverityIcon = (sev) => {
        if(sev === 'Critical') return `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-danger)" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;
        if(sev === 'Warning') return `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-warning)" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`;
        return `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`;
    };

    const getStatusChip = (status) => {
        switch(status) {
            case 'Unread': return `<span class="status-chip status-chip-danger">Unread</span>`;
            case 'Open': return `<span class="status-chip status-chip-warning">Open</span>`;
            case 'Acknowledged': return `<span class="status-chip status-chip-info">Acknowledged</span>`;
            case 'Resolved': return `<span class="status-chip status-chip-success">Resolved</span>`;
            default: return `<span class="status-chip">${status}</span>`;
        }
    };

    // Render Table and Mobile Cards
    const renderData = (data) => {
        const tbody = document.getElementById('alertsTableBody');
        const mobileContainer = document.getElementById('alertMobileCardsContainer');
        
        tbody.innerHTML = '';
        mobileContainer.innerHTML = '';

        if(data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 40px; color: var(--color-text-muted);">No alerts found matching your filters.</td></tr>`;
            mobileContainer.innerHTML = `<div style="text-align:center; padding: 40px; color: var(--color-text-muted);">No alerts found matching your filters.</div>`;
            return;
        }

        data.forEach(alert => {
            // Desktop Row
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div style="font-weight: 600; margin-bottom: 2px;">${alert.title}</div>
                    <div style="font-size: 12px; color: var(--color-text-muted);">${alert.id} • ${alert.entity}</div>
                </td>
                <td>
                    <div style="display:flex; align-items:center; gap:6px;" class="severity-${alert.severity.toLowerCase()}">
                        ${getSeverityIcon(alert.severity)}
                        ${alert.severity}
                    </div>
                </td>
                <td>${alert.source}</td>
                <td><span style="font-size: 13px; color: var(--color-text-muted);">${alert.timestamp}</span></td>
                <td>${getStatusChip(alert.status)}</td>
                <td>
                    <button class="btn-text btn-action" style="padding: 4px 8px; font-size: 13px;" onclick="event.stopPropagation(); window.showToast('Alert Acknowledged.', 'info')">Ack</button>
                </td>
            `;
            tr.addEventListener('click', () => openDetailPanel(alert));
            tbody.appendChild(tr);

            // Mobile Card
            const card = document.createElement('div');
            card.className = 'alert-mobile-card';
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <div style="font-weight: 600; font-family: 'Outfit', sans-serif;">${alert.title}</div>
                        <div style="font-size: 12px; color: var(--color-text-muted);">${alert.id}</div>
                    </div>
                    ${getStatusChip(alert.status)}
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; margin-bottom: 12px;">
                    <div style="display:flex; align-items:center; gap:4px;" class="severity-${alert.severity.toLowerCase()}">${getSeverityIcon(alert.severity)} ${alert.severity}</div>
                    <div><span style="color: var(--color-text-muted);">Source:</span> ${alert.source}</div>
                    <div style="grid-column: span 2;"><span style="color: var(--color-text-muted);">Entity:</span> ${alert.entity}</div>
                    <div style="grid-column: span 2; color: var(--color-text-muted);">${alert.timestamp}</div>
                </div>
                <button class="btn btn-secondary" style="width: 100%;">View Details</button>
            `;
            card.addEventListener('click', () => openDetailPanel(alert));
            mobileContainer.appendChild(card);
        });
    };

    // Filter Logic
    const filterData = () => {
        const search = document.getElementById('alertSearch').value.toLowerCase();
        const severity = document.getElementById('filterSeverity').value;
        const source = document.getElementById('filterSource').value;
        const status = document.getElementById('filterStatus').value;

        const filtered = MOCK_ALERTS.filter(alert => {
            const matchSearch = alert.title.toLowerCase().includes(search) || alert.id.toLowerCase().includes(search) || alert.entity.toLowerCase().includes(search);
            const matchSev = severity === 'all' || alert.severity === severity;
            const matchSrc = source === 'all' || alert.source.includes(source); // allow partial match like OCR for OCR / ANPR
            const matchStat = status === 'all' || alert.status === status;

            return matchSearch && matchSev && matchSrc && matchStat;
        });

        renderData(filtered);
    };

    document.getElementById('alertSearch').addEventListener('input', filterData);
    document.getElementById('filterSeverity').addEventListener('change', filterData);
    document.getElementById('filterSource').addEventListener('change', filterData);
    document.getElementById('filterStatus').addEventListener('change', filterData);
    document.getElementById('clearAlertFiltersBtn').addEventListener('click', () => {
        document.getElementById('alertSearch').value = '';
        document.getElementById('filterSeverity').value = 'all';
        document.getElementById('filterSource').value = 'all';
        document.getElementById('filterStatus').value = 'all';
        filterData();
    });

    // Detail Panel Logic
    const panel = document.getElementById('alertDetailPanel');
    const closeBtn = document.getElementById('closeAlertDetailBtn');

    const openDetailPanel = (alert) => {
        document.getElementById('detAlertTitle').innerText = alert.title;
        document.getElementById('detAlertId').innerText = alert.id;
        document.getElementById('detAlertTime').innerText = alert.timestamp;
        
        const sevHtml = `<span class="status-chip" style="background:transparent; border:1px solid currentColor;" class="severity-${alert.severity.toLowerCase()}">${getSeverityIcon(alert.severity)} ${alert.severity}</span>`;
        document.getElementById('detAlertChips').innerHTML = sevHtml + getStatusChip(alert.status);
        
        document.getElementById('detAlertEntity').innerText = `${alert.source} • ${alert.entity}`;
        document.getElementById('detAlertDesc').innerText = alert.desc;
        document.getElementById('detAlertAction').innerText = alert.action;

        panel.classList.add('active');
    };

    closeBtn.addEventListener('click', () => {
        panel.classList.remove('active');
    });

    // Boot
    renderData(MOCK_ALERTS);
});
