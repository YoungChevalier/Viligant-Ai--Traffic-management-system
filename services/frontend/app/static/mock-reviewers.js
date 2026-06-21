/**
 * Mock Reviewers Logic
 */

document.addEventListener('DOMContentLoaded', () => {

    const MOCK_REVIEWERS = [
        { id: "REV-1042", name: "R. Vargas", role: "Senior Reviewer", status: "Online", workload: "Medium", assigned: 24, closed: 142, avgTime: "1m 20s", appr: 68, esc: 8, lastActive: "Just now", specs: ["Red-Light", "Speeding"], splits: [68, 24, 8] },
        { id: "REV-1089", name: "A. Smith", role: "Reviewer", status: "Online", workload: "Low", assigned: 5, closed: 89, avgTime: "2m 15s", appr: 72, esc: 5, lastActive: "2 mins ago", specs: ["Helmet"], splits: [72, 23, 5] },
        { id: "REV-0922", name: "J. Doe", role: "Reviewer", status: "Busy", workload: "Overloaded", assigned: 85, closed: 210, avgTime: "1m 05s", appr: 80, esc: 2, lastActive: "Just now", specs: ["Stop-Line", "Wrong-Side"], splits: [80, 18, 2] },
        { id: "REV-1105", name: "S. Lee", role: "Supervisor", status: "Online", workload: "Low", assigned: 2, closed: 15, avgTime: "3m 40s", appr: 45, esc: 15, lastActive: "Just now", specs: ["Escalations"], splits: [45, 40, 15] },
        { id: "REV-1055", name: "M. Johnson", role: "Reviewer", status: "On break", workload: "Medium", assigned: 18, closed: 65, avgTime: "1m 55s", appr: 65, esc: 10, lastActive: "15 mins ago", specs: ["Illegal Parking"], splits: [65, 25, 10] },
        { id: "REV-0988", name: "L. Chen", role: "Senior Reviewer", status: "Offline", workload: "Low", assigned: 0, closed: 0, avgTime: "-", appr: 0, esc: 0, lastActive: "2 hours ago", specs: ["Speeding", "Red-Light"], splits: [0, 0, 0] },
        { id: "REV-1021", name: "D. Patel", role: "Reviewer", status: "Online", workload: "High", assigned: 45, closed: 180, avgTime: "1m 30s", appr: 70, esc: 6, lastActive: "Just now", specs: ["Triple Riding", "Helmet"], splits: [70, 24, 6] },
        { id: "REV-1112", name: "E. Wright", role: "Reviewer", status: "Busy", workload: "Overloaded", assigned: 72, closed: 130, avgTime: "2m 10s", appr: 55, esc: 12, lastActive: "1 min ago", specs: ["Wrong-Side"], splits: [55, 33, 12] },
        { id: "REV-0945", name: "K. Gomez", role: "Supervisor", status: "Offline", workload: "Low", assigned: 0, closed: 42, avgTime: "4m 15s", appr: 50, esc: 5, lastActive: "1 day ago", specs: ["Escalations", "Audits"], splits: [50, 45, 5] },
        { id: "REV-1150", name: "R. Kim", role: "Reviewer", status: "Online", workload: "Medium", assigned: 20, closed: 110, avgTime: "1m 45s", appr: 62, esc: 9, lastActive: "Just now", specs: ["Stop-Line", "Illegal Parking"], splits: [62, 29, 9] }
    ];

    const getStatusChip = (status) => {
        switch(status) {
            case 'Online': return `<span class="status-chip status-chip-success">Online</span>`;
            case 'Offline': return `<span class="status-chip status-chip-danger">Offline</span>`;
            case 'Busy': return `<span class="status-chip status-chip-warning">Busy</span>`;
            case 'On break': return `<span class="status-chip status-chip-warning" style="background:transparent; border:1px solid var(--color-warning);">On break</span>`;
            default: return `<span class="status-chip">${status}</span>`;
        }
    };

    const getWorkloadChip = (workload) => {
        switch(workload) {
            case 'Low': return `<span class="status-chip status-chip-success" style="background:transparent; border:1px solid var(--color-success);">Low</span>`;
            case 'Medium': return `<span class="status-chip status-chip-warning" style="background:transparent; border:1px solid var(--color-warning);">Medium</span>`;
            case 'High': return `<span class="status-chip status-chip-danger" style="background:transparent; border:1px solid var(--color-danger);">High</span>`;
            case 'Overloaded': return `<span class="status-chip status-chip-danger">Overloaded</span>`;
            default: return `<span class="status-chip">${workload}</span>`;
        }
    };

    const getInitials = (name) => {
        const parts = name.split(' ');
        if(parts.length > 1) return (parts[0][0] + parts[1][0]).toUpperCase();
        return name.substring(0, 2).toUpperCase();
    };

    // Render Table and Mobile Cards
    const renderData = (data) => {
        const tbody = document.getElementById('reviewersTableBody');
        const mobileContainer = document.getElementById('revMobileCardsContainer');
        
        tbody.innerHTML = '';
        mobileContainer.innerHTML = '';

        if(data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 40px; color: var(--color-text-muted);">No reviewers found matching your filters.</td></tr>`;
            mobileContainer.innerHTML = `<div style="text-align:center; padding: 40px; color: var(--color-text-muted);">No reviewers found matching your filters.</div>`;
            return;
        }

        data.forEach(rev => {
            // Desktop Row
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:12px;">
                        <div class="avatar" style="width: 32px; height: 32px; background: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 600; font-size: 12px;">${getInitials(rev.name)}</div>
                        <div>
                            <div style="font-weight: 600;">${rev.name}</div>
                            <div style="font-size: 12px; color: var(--color-text-muted);">${rev.id}</div>
                        </div>
                    </div>
                </td>
                <td>
                    <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                        <span style="font-size: 13px;">${rev.role}</span>
                        ${getStatusChip(rev.status)}
                    </div>
                </td>
                <td>${getWorkloadChip(rev.workload)}</td>
                <td><strong>${rev.closed}</strong> <span style="color:var(--color-text-muted); font-size:12px;">/ ${rev.assigned} open</span></td>
                <td>${rev.avgTime}</td>
                <td>
                    <span class="text-success">${rev.appr}%</span> / <span class="text-warning">${rev.esc}%</span>
                </td>
                <td><span style="font-size: 13px; color: var(--color-text-muted);">${rev.lastActive}</span></td>
                <td>
                    <button class="btn-text btn-action" style="padding: 4px 8px; font-size: 13px;" onclick="event.stopPropagation(); window.showToast('Ping sent to reviewer.', 'success')">Ping</button>
                </td>
            `;
            tr.addEventListener('click', () => openDetailPanel(rev));
            tbody.appendChild(tr);

            // Mobile Card
            const card = document.createElement('div');
            card.className = 'reviewer-mobile-card';
            card.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <div class="avatar" style="width: 32px; height: 32px; background: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-weight: 600; font-size: 12px;">${getInitials(rev.name)}</div>
                        <div>
                            <span style="font-weight: 600; font-family: 'Outfit', sans-serif;">${rev.name}</span>
                            <div style="font-size: 12px; color: var(--color-text-muted);">${rev.role}</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 4px; flex-direction: column; align-items: flex-end;">${getStatusChip(rev.status)}${getWorkloadChip(rev.workload)}</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; margin-bottom: 16px;">
                    <div><span style="color: var(--color-text-muted);">Closed/Open:</span> <strong>${rev.closed}</strong> / ${rev.assigned}</div>
                    <div><span style="color: var(--color-text-muted);">Avg Time:</span> <strong>${rev.avgTime}</strong></div>
                    <div><span style="color: var(--color-text-muted);">Appr/Esc:</span> <strong class="text-success">${rev.appr}%</strong> / <strong class="text-warning">${rev.esc}%</strong></div>
                    <div><span style="color: var(--color-text-muted);">Active:</span> <strong>${rev.lastActive}</strong></div>
                </div>
                <button class="btn btn-secondary" style="width: 100%;">View Details</button>
            `;
            card.addEventListener('click', () => openDetailPanel(rev));
            mobileContainer.appendChild(card);
        });
    };

    // Filter Logic
    const filterData = () => {
        const search = document.getElementById('revSearch').value.toLowerCase();
        const status = document.getElementById('filterStatus').value;
        const role = document.getElementById('filterRole').value;
        const workload = document.getElementById('filterWorkload').value;

        const filtered = MOCK_REVIEWERS.filter(rev => {
            const matchSearch = rev.name.toLowerCase().includes(search) || rev.id.toLowerCase().includes(search);
            const matchStatus = status === 'all' || rev.status === status;
            
            // Allow exact matching or partial (e.g., 'Senior Reviewer' vs 'Senior')
            let matchRole = role === 'all' || rev.role === role;
            if(role === 'Senior Reviewer' && rev.role === 'Senior Reviewer') matchRole = true;
            else if(role === 'Reviewer' && rev.role === 'Reviewer') matchRole = true;
            else if(role === 'Supervisor' && rev.role === 'Supervisor') matchRole = true;

            const matchWorkload = workload === 'all' || rev.workload === workload;
            return matchSearch && matchStatus && matchRole && matchWorkload;
        });

        renderData(filtered);
    };

    document.getElementById('revSearch').addEventListener('input', filterData);
    document.getElementById('filterStatus').addEventListener('change', filterData);
    document.getElementById('filterRole').addEventListener('change', filterData);
    document.getElementById('filterWorkload').addEventListener('change', filterData);
    document.getElementById('clearRevFiltersBtn').addEventListener('click', () => {
        document.getElementById('revSearch').value = '';
        document.getElementById('filterStatus').value = 'all';
        document.getElementById('filterRole').value = 'all';
        document.getElementById('filterWorkload').value = 'all';
        filterData();
    });

    // Detail Panel Logic
    const panel = document.getElementById('reviewerDetailPanel');
    const closeBtn = document.getElementById('closeRevDetailBtn');

    const openDetailPanel = (rev) => {
        document.getElementById('detRevInitials').innerText = getInitials(rev.name);
        document.getElementById('detRevName').innerText = rev.name;
        document.getElementById('detRevId').innerText = `${rev.id} • ${rev.role}`;
        
        document.getElementById('detRevChips').innerHTML = getStatusChip(rev.status) + getWorkloadChip(rev.workload);
        
        document.getElementById('detRevAssigned').innerText = rev.assigned;
        document.getElementById('detRevClosed').innerText = rev.closed;
        document.getElementById('detRevTime').innerText = rev.avgTime;
        
        document.getElementById('detRevRates').innerText = `${rev.splits[0]}% / ${rev.splits[1]}% / ${rev.splits[2]}%`;
        
        // Split Bar
        document.getElementById('detRevSplitBar').innerHTML = `
            <div style="background: var(--color-success); width: ${rev.splits[0]}%;"></div>
            <div style="background: var(--color-text-muted); width: ${rev.splits[1]}%;"></div>
            <div style="background: var(--color-warning); width: ${rev.splits[2]}%;"></div>
        `;

        // Specializations
        document.getElementById('detRevSpecs').innerHTML = rev.specs.map(s => 
            `<span style="background: var(--color-bg-base); padding: 4px 8px; border-radius: 4px; border: 1px solid var(--color-border); font-size: 12px;">${s}</span>`
        ).join('');

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
    renderData(MOCK_REVIEWERS);
});
