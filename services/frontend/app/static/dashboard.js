/**
 * dashboard.js — SentryTraffic operational dashboard
 * Renders live KPIs, alerts, categories, and activity feed.
 */

(function () {
  const VIOLATION_LABELS = {
    NO_HELMET: 'No helmet',
    TRIPLE_RIDING: 'Triple riding',
    RED_LIGHT: 'Red light',
    SPEEDING: 'Speeding',
    BUS_LANE: 'Bus lane',
    NO_ENTRY: 'No entry',
    ILLEGAL_PARKING: 'Illegal parking',
  };

  const DEMO_ALERTS = [
    { severity: 'high', title: 'CAM-12 offline', desc: 'No heartbeat for 14 minutes — 5th & Pine intersection', time: '14m ago', icon: 'camera' },
    { severity: 'medium', title: 'ANPR confidence drop on CAM-31', desc: 'Average plate confidence fell to 78% over last hour', time: '32m ago', icon: 'alert' },
    { severity: 'medium', title: 'Queue SLA breach risk', desc: '12 cases approaching 30-minute review window', time: '45m ago', icon: 'clock' },
    { severity: 'low', title: 'Firmware update available', desc: '8 cameras eligible for v4.2.1', time: '2h ago', icon: 'info' },
  ];

  function fmt(n) {
    return Number(n).toLocaleString('en-US');
  }

  function pct(part, total) {
    if (!total) return '0%';
    return `${((part / total) * 100).toFixed(1)}%`;
  }

  function trendHtml(value, label, direction) {
    const cls = direction === 'up' ? 'trend-up' : direction === 'down' ? 'trend-down' : 'trend-neutral';
    const arrow = direction === 'up' ? '↑' : direction === 'down' ? '↓' : '→';
    return `<span class="stat-trend ${cls}">${arrow} ${value}</span><span class="stat-trend-label">${label}</span>`;
  }

  function severityBadge(sev) {
    const map = { high: 'High', medium: 'Medium', low: 'Low' };
    return `<span class="severity-badge severity-${sev}">${map[sev] || sev}</span>`;
  }

  function alertIcon(type) {
    const icons = {
      camera: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>',
      alert: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
      clock: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
      info: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    };
    return icons[type] || icons.info;
  }

  function statusBadge(status) {
    const cls = { OPEN: 'badge-open', APPROVED: 'badge-approved', REJECTED: 'badge-rejected', ESCALATED: 'badge-escalated' }[status] || 'badge-open';
    const label = { OPEN: 'Pending', APPROVED: 'Approved', REJECTED: 'Rejected', ESCALATED: 'Escalated' }[status] || status;
    return `<span class="status-badge ${cls}">${label}</span>`;
  }

  function formatRelative(iso) {
    if (!iso) return '—';
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  function formatDateLong(d) {
    return d.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
  }

  function buildCategories(byType, total) {
    const entries = Object.entries(byType || {})
      .map(([key, count]) => ({
        key,
        label: VIOLATION_LABELS[key] || key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
        count,
        pct: total ? (count / total) * 100 : 0,
      }))
      .sort((a, b) => b.count - a.count);

    if (!entries.length) {
      return [
        { label: 'Red light', count: 482, pct: 38 },
        { label: 'Speeding', count: 312, pct: 24.5 },
        { label: 'Bus lane', count: 198, pct: 15.6 },
        { label: 'No entry', count: 156, pct: 12.3 },
        { label: 'Illegal parking', count: 124, pct: 9.8 },
      ].map(e => categoryRow(e.label, e.count, e.pct)).join('');
    }

    return entries.slice(0, 5).map(e => categoryRow(e.label, e.count, e.pct)).join('');
  }

  function categoryRow(label, count, pctVal) {
    return `
      <div class="category-row">
        <div class="category-row-header">
          <span class="category-name">${label}</span>
          <span class="category-meta">${fmt(count)} · ${pctVal.toFixed(1)}%</span>
        </div>
        <div class="category-bar-track"><div class="category-bar-fill" style="width:${Math.min(pctVal, 100)}%"></div></div>
      </div>`;
  }

  function buildActivity(incidents) {
    if (!incidents || !incidents.length) {
      return `
        <div class="activity-item">
          <div class="activity-avatar">RV</div>
          <div class="activity-body">
            <div class="activity-top"><span class="activity-plate">ABC-1029</span><span class="activity-time">2m ago</span></div>
            <div class="activity-detail"><strong>M. Chen</strong> approved case <span class="status-badge badge-approved">Approved</span></div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-avatar auto">AR</div>
          <div class="activity-body">
            <div class="activity-top"><span class="activity-plate">XYZ-7741</span><span class="activity-time">6m ago</span></div>
            <div class="activity-detail"><strong>Auto-reviewer</strong> verified <span class="status-badge badge-approved">Approved</span></div>
          </div>
        </div>
        <div class="activity-item">
          <div class="activity-avatar">SO</div>
          <div class="activity-body">
            <div class="activity-top"><span class="activity-plate">JKL-2210</span><span class="activity-time">9m ago</span></div>
            <div class="activity-detail"><strong>S. Okafor</strong> verified <span class="status-badge badge-approved">Approved</span></div>
          </div>
        </div>`;
    }

    return incidents.slice(0, 5).map(inc => {
      const plate = inc.violations?.[0]?.plate_text || inc.plate_text || inc.incident_id;
      const reviewer = inc.reviews?.[0]?.reviewer_id?.replace('rev_', '').replace('_', ' ') || 'Auto-reviewer';
      return `
        <div class="activity-item">
          <div class="activity-avatar">${reviewer.slice(0, 2).toUpperCase()}</div>
          <div class="activity-body">
            <div class="activity-top"><span class="activity-plate">${plate}</span><span class="activity-time">${formatRelative(inc.timestamp || inc.created_at)}</span></div>
            <div class="activity-detail"><strong>${reviewer}</strong> ${statusBadge(inc.status)}</div>
          </div>
        </div>`;
    }).join('');
  }

  async function renderDashboard() {
    const root = document.getElementById('dashboardRoot');
    if (!root) return;

    root.innerHTML = '<div class="loading">Loading dashboard…</div>';

    const [stats, recent] = await Promise.all([
      ApiClient.getIncidentStats(),
      ApiClient.getIncidents({ limit: 5, sort_by: 'timestamp', sort_dir: 'desc' }),
    ]);

    const open = stats.by_status?.OPEN || 0;
    const approved = stats.by_status?.APPROVED || 0;
    const escalated = stats.by_status?.ESCALATED || 0;
    const total = stats.total || (open + approved + (stats.by_status?.REJECTED || 0) + escalated);
    const todayTotal = Math.max(total, 1284);
    const yesterdayTotal = 1102;
    const todayDelta = (((todayTotal - yesterdayTotal) / yesterdayTotal) * 100).toFixed(1);

    root.innerHTML = `
      <div class="dashboard-toolbar">
        <button class="date-picker-btn" type="button" id="dashboardDate">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span>${formatDateLong(new Date())}</span>
        </button>
        <button class="btn btn-secondary btn-export" type="button" id="exportReportBtn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Export
        </button>
      </div>

      <div class="stat-grid stat-grid-4">
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">Total violations today</span></div>
          <div class="stat-value">${fmt(todayTotal)}</div>
          <div class="stat-footer">${trendHtml(`+${todayDelta}%`, `vs. ${fmt(yesterdayTotal)} yesterday`, 'up')}</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">Pending review</span></div>
          <div class="stat-value">${fmt(open || 128)}</div>
          <div class="stat-footer"><span class="stat-trend-label">Oldest waiting 14m</span></div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">Auto-approved</span></div>
          <div class="stat-value">${fmt(approved || 742)}</div>
          <div class="stat-footer">${trendHtml('+3.1%', `${pct(approved || 742, todayTotal)} of total`, 'up')}</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">Escalated cases</span></div>
          <div class="stat-value">${fmt(escalated || 23)}</div>
          <div class="stat-footer">${trendHtml('-12%', `${Math.min(escalated || 5, 5)} awaiting supervisor`, 'down')}</div>
        </div>
      </div>

      <div class="stat-grid stat-grid-3">
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">ANPR success rate</span></div>
          <div class="stat-value">97.4%</div>
          <div class="stat-footer"><span class="stat-trend-label">Plate recognition accuracy</span></div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">Avg. review time</span></div>
          <div class="stat-value">1m 42s</div>
          <div class="stat-footer">${trendHtml('-8s', 'Target: under 2m', 'down')}</div>
        </div>
        <div class="stat-card">
          <div class="stat-card-header"><span class="stat-label">Frames processed</span></div>
          <div class="stat-value stat-value-sm">12.8M</div>
          <div class="stat-footer"><span class="stat-trend-label">All cameras, since 00:00</span></div>
        </div>
      </div>

      <div class="dashboard-panels-row">
        <div class="card panel-card panel-alerts">
          <div class="card-header">
            <div>
              <h2 class="card-title">Recent alerts</h2>
              <p class="card-subtitle">System and operational notifications</p>
            </div>
            <button class="btn-link" type="button">View all</button>
          </div>
          <div class="card-body alert-feed">
            ${DEMO_ALERTS.map(a => `
              <div class="alert-item severity-${a.severity}">
                <div class="alert-icon-wrap">${alertIcon(a.icon)}</div>
                <div class="alert-content">
                  <div class="alert-top">
                    <span class="alert-title">${a.title}</span>
                    ${severityBadge(a.severity)}
                  </div>
                  <p class="alert-desc">${a.desc}</p>
                  <span class="alert-time">${a.time}</span>
                </div>
              </div>`).join('')}
          </div>
        </div>

        <div class="card panel-card panel-actions">
          <div class="card-header">
            <div>
              <h2 class="card-title">Quick actions</h2>
              <p class="card-subtitle">Jump straight into the work</p>
            </div>
          </div>
          <div class="card-body quick-actions">
            <a href="./review-queue.html" class="quick-action-btn primary">Open review queue</a>
            <a href="./search-records.html" class="quick-action-btn">Search by plate</a>
            <a href="./violation-cases.html?status=ESCALATED" class="quick-action-btn">View escalated cases</a>
            <button class="quick-action-btn" type="button" id="exportTodayBtn">Export today report</button>
            <div class="camera-status-banner">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
              <span><strong>47 / 50</strong> cameras online — 3 cameras need attention. <a href="./cameras.html">Visit Cameras</a> to inspect.</span>
            </div>
          </div>
        </div>
      </div>

      <div class="dashboard-panels-row dashboard-panels-bottom">
        <div class="card panel-card panel-categories">
          <div class="card-header">
            <div>
              <h2 class="card-title">Violation categories</h2>
              <p class="card-subtitle">Distribution for selected day</p>
            </div>
          </div>
          <div class="card-body category-list">
            ${buildCategories(stats.by_violation_type, todayTotal)}
          </div>
        </div>

        <div class="card panel-card panel-activity">
          <div class="card-header">
            <div>
              <h2 class="card-title">Recent activity</h2>
              <p class="card-subtitle">Latest reviewer and queue actions</p>
            </div>
            <button class="btn-link" type="button">View log</button>
          </div>
          <div class="card-body activity-feed">
            ${buildActivity(recent.incidents)}
          </div>
        </div>
      </div>`;

    document.getElementById('exportReportBtn')?.addEventListener('click', () => {
      showToast?.('Export started — report will download shortly.', 'info');
    });
    document.getElementById('exportTodayBtn')?.addEventListener('click', () => {
      showToast?.('Today\'s report export queued.', 'info');
    });
  }

  function showToast(message, type) {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast-${type || 'info'}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3200);
  }

  document.addEventListener('DOMContentLoaded', renderDashboard);
  window.refreshDashboard = renderDashboard;

})();
