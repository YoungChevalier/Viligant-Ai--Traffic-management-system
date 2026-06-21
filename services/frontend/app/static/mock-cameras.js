/**
 * Mock Cameras Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    let MOCK_CAMERAS = [];

    const getStatusChip = (status) => {
        switch(status) {
            case 'Active': return `<span class="status-chip status-chip-success">Active</span>`;
            case 'Offline': return `<span class="status-chip status-chip-danger">Offline</span>`;
            case 'Maintenance': return `<span class="status-chip status-chip-warning">Maintenance</span>`;
            case 'Degraded': return `<span class="status-chip status-chip-warning">Degraded</span>`;
            default: return `<span class="status-chip">${status}</span>`;
        }
    };

    const getHealthChip = (health) => {
        switch(health) {
            case 'Healthy': return `<span class="status-chip status-chip-success" style="background:transparent; border:1px solid var(--color-success);">Healthy</span>`;
            case 'Warning': return `<span class="status-chip status-chip-warning" style="background:transparent; border:1px solid var(--color-warning);">Warning</span>`;
            case 'Critical': return `<span class="status-chip status-chip-danger" style="background:transparent; border:1px solid var(--color-danger);">Critical</span>`;
            default: return `<span class="status-chip">${health}</span>`;
        }
    };

    // Render Table and Mobile Cards
    const renderData = (data) => {
        const tbody = document.getElementById('camerasTableBody');
        const mobileContainer = document.getElementById('mobileCardsContainer');
        
        tbody.innerHTML = '';
        mobileContainer.innerHTML = '';

        if(data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color: var(--color-text-muted);">No cameras found matching your filters.</td></tr>`;
            mobileContainer.innerHTML = `<div style="text-align:center; padding: 40px; color: var(--color-text-muted);">No cameras found matching your filters.</div>`;
            return;
        }

        data.forEach(cam => {
            // Desktop Row
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="font-weight: 600;">${cam.id}</td>
                <td>
                    <div>${cam.loc}</div>
                    <div style="font-size: 12px; color: var(--color-text-muted);">${cam.zone} Zone</div>
                </td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        ${getStatusChip(cam.status)}
                        ${getHealthChip(cam.health)}
                    </div>
                </td>
                <td>${cam.vToday}</td>
                <td><span class="${cam.ocr > 90 ? 'text-success' : (cam.ocr > 70 ? 'text-warning' : 'text-danger')}">${cam.ocr}%</span></td>
                <td><span style="font-size: 13px; color: var(--color-text-muted);">${cam.sync}</span></td>
                <td>
                    <button class="btn-text btn-action" style="padding: 4px 8px; font-size: 13px;" onclick="event.stopPropagation(); window.showToast('Camera diagnostics initiated.', 'success')">Ping</button>
                </td>
            `;
            tr.addEventListener('click', () => openDetailPanel(cam));
            tbody.appendChild(tr);

            // Mobile Card
            const card = document.createElement('div');
            card.className = 'camera-mobile-card';
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-weight: 600; font-family: 'Outfit', sans-serif;">${cam.id}</span>
                    <div style="display: flex; gap: 4px;">${getStatusChip(cam.status)}${getHealthChip(cam.health)}</div>
                </div>
                <div style="color: var(--color-text-muted); font-size: 13px; margin-bottom: 16px;">${cam.loc} • ${cam.zone} Zone</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; margin-bottom: 16px;">
                    <div><span style="color: var(--color-text-muted);">Violations:</span> <strong>${cam.vToday}</strong></div>
                    <div><span style="color: var(--color-text-muted);">OCR:</span> <strong class="${cam.ocr > 90 ? 'text-success' : 'text-danger'}">${cam.ocr}%</strong></div>
                    <div><span style="color: var(--color-text-muted);">Last Sync:</span> <strong>${cam.sync}</strong></div>
                </div>
                <button class="btn btn-secondary" style="width: 100%;">View Details</button>
            `;
            card.addEventListener('click', () => openDetailPanel(cam));
            mobileContainer.appendChild(card);
        });
    };

    // Filter Logic
    const filterData = () => {
        const search = document.getElementById('camSearch').value.toLowerCase();
        const status = document.getElementById('filterStatus').value;
        const zone = document.getElementById('filterZone').value;
        const health = document.getElementById('filterHealth').value;

        const filtered = MOCK_CAMERAS.filter(cam => {
            const matchSearch = cam.id.toLowerCase().includes(search) || cam.loc.toLowerCase().includes(search);
            const matchStatus = status === 'all' || cam.status === status;
            const matchZone = zone === 'all' || cam.zone === zone;
            const matchHealth = health === 'all' || cam.health === health;
            return matchSearch && matchStatus && matchZone && matchHealth;
        });

        renderData(filtered);
    };

    document.getElementById('camSearch').addEventListener('input', filterData);
    document.getElementById('filterStatus').addEventListener('change', filterData);
    document.getElementById('filterZone').addEventListener('change', filterData);
    document.getElementById('filterHealth').addEventListener('change', filterData);
    document.getElementById('clearFiltersBtn').addEventListener('click', () => {
        document.getElementById('camSearch').value = '';
        document.getElementById('filterStatus').value = 'all';
        document.getElementById('filterZone').value = 'all';
        document.getElementById('filterHealth').value = 'all';
        filterData();
    });

    // Detail Panel Logic
    const panel = document.getElementById('cameraDetailPanel');
    const closeBtn = document.getElementById('closeDetailBtn');

    const openDetailPanel = (cam) => {
        document.getElementById('detCamId').innerText = cam.id;
        document.getElementById('detLoc').innerText = `${cam.loc} • ${cam.zone} Zone`;
        document.getElementById('detStatusChips').innerHTML = getStatusChip(cam.status) + getHealthChip(cam.health);
        document.getElementById('detSync').innerText = cam.sync;
        document.getElementById('detQuality').innerText = cam.quality;
        document.getElementById('detViolations').innerText = cam.vToday;
        document.getElementById('detOcr').innerText = cam.ocr + '%';
        document.getElementById('detOcr').className = 'meta-value ' + (cam.ocr > 90 ? 'text-success' : 'text-danger');
        document.getElementById('detTypes').innerText = cam.types;

        // Alerts
        const alertContainer = document.getElementById('detAlerts');
        if(cam.alerts.length === 0) {
            alertContainer.innerHTML = `<span style="font-size:13px; color:var(--color-text-muted);">No active alerts. System healthy.</span>`;
        } else {
            alertContainer.innerHTML = cam.alerts.map(a => `
                <div style="background: rgba(239, 68, 68, 0.1); border-left: 3px solid var(--color-danger); padding: 12px; margin-bottom: 8px; border-radius: 4px; font-size: 13px;">
                    ${a}
                </div>
            `).join('');
        }

        // Mini Analytics OCR Bar
        document.getElementById('detOcrBar').innerHTML = `
            <div style="background: var(--color-success); width: ${cam.ocrBars[0]}%;"></div>
            <div style="background: var(--color-warning); width: ${cam.ocrBars[1]}%;"></div>
            <div style="background: var(--color-danger); width: ${cam.ocrBars[2]}%;"></div>
            <div style="background: var(--color-text-muted); width: ${cam.ocrBars[3]}%;"></div>
        `;

        panel.classList.add('active');
    };

    closeBtn.addEventListener('click', () => {
        panel.classList.remove('active');
    });

    // Toast Utility (fallback if not in app.js)
    window.showToast = window.showToast || ((message, type = 'success') => {
        let container = document.getElementById('toastContainer');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toastContainer';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = 'toast show';
        if(type === 'error' || type === 'danger') toast.style.borderLeftColor = 'var(--color-danger)';
        if(type === 'warning') toast.style.borderLeftColor = 'var(--color-warning)';
        toast.innerText = message;
        
        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    });

    // Boot
    const boot = async () => {
        try {
            const apiData = await ApiClient.getCameras();
            MOCK_CAMERAS = apiData.map(c => ({
                id: c.id,
                loc: c.name,
                zone: c.zone,
                status: c.status,
                health: c.health > 80 ? 'Healthy' : (c.health > 40 ? 'Warning' : 'Critical'),
                quality: "1080p",
                vToday: Math.floor(Math.random() * 200), // mock this for now
                ocr: Math.floor(Math.random() * 20) + 80, // mock this
                sync: "Just now",
                types: "Various",
                alerts: c.status === 'Offline' ? ["Offline"] : [],
                ocrBars: [85, 10, 3, 2]
            }));
            renderData(MOCK_CAMERAS);
        } catch (e) {
            console.error("Failed to fetch cameras", e);
        }
    };
    boot();
});
