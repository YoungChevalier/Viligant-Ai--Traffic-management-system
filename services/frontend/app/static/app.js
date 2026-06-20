/**
 * app.js — SPA Controller for Traffic Violation Reviewer Dashboard
 *
 * Hash-based routing:
 *   #dashboard  — KPI summary + overview charts
 *   #cases      — Filterable, paginated case list
 *   #case/:id   — Case detail with evidence + reviewer history + decision form
 *   #analytics  — Analytics view with charts and filters
 */

// ── State ──────────────────────────────────────────────────────────────────
const state = {
  currentPage: 1,
  pageSize: 10,
  filters: {},
  sortBy: "timestamp",
  sortDir: "desc",
};

// ── DOM Helpers ────────────────────────────────────────────────────────────
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "className") node.className = v;
    else if (k === "innerHTML") node.innerHTML = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2).toLowerCase(), v);
    else node.setAttribute(k, v);
  }
  children.forEach(c => {
    if (typeof c === "string") node.appendChild(document.createTextNode(c));
    else if (c) node.appendChild(c);
  });
  return node;
}

function html(parent, htmlStr) {
  parent.innerHTML = htmlStr;
}

// ── Toast System ───────────────────────────────────────────────────────────
function showToast(message, type = "info") {
  let container = $(".toast-container");
  if (!container) {
    container = el("div", { className: "toast-container" });
    document.body.appendChild(container);
  }
  const toast = el("div", { className: `toast toast-${type}` }, [message]);
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

// ── Formatting Helpers ─────────────────────────────────────────────────────
function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("en-IN", {
    year: "numeric", month: "short", day: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

function formatDateShort(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("en-IN", { month: "short", day: "numeric" });
}

function statusBadge(status) {
  const cls = {
    OPEN: "badge-open", APPROVED: "badge-approved",
    REJECTED: "badge-rejected", ESCALATED: "badge-escalated",
  }[status] || "badge-open";
  return `<span class="badge ${cls}">${status}</span>`;
}

function confidenceBar(value) {
  if (value === null || value === undefined) return "—";
  const pct = Math.round(value * 100);
  const color = pct >= 90 ? "#22c55e" : pct >= 75 ? "#f59e0b" : "#ef4444";
  return `<span class="confidence-bar">
    <span class="bar-track"><span class="bar-fill" style="width:${pct}%;background:${color}"></span></span>
    <span class="bar-label">${pct}%</span>
  </span>`;
}

// ── Router ─────────────────────────────────────────────────────────────────
function getRoute() {
  const hash = window.location.hash || "#dashboard";
  if (hash.startsWith("#case/")) return { view: "case-detail", id: hash.slice(6) };
  if (hash === "#cases") return { view: "cases" };
  if (hash === "#analytics") return { view: "analytics" };
  return { view: "dashboard" };
}

function navigate(hash) {
  window.location.hash = hash;
}

function updateNav() {
  const route = getRoute();
  $$(".sidebar-nav a").forEach(a => {
    const target = a.getAttribute("href");
    const isActive = (route.view === "dashboard" && target === "#dashboard")
      || (route.view === "cases" && target === "#cases")
      || (route.view === "case-detail" && target === "#cases")
      || (route.view === "analytics" && target === "#analytics");
    a.classList.toggle("active", isActive);
  });
}

async function routeToView() {
  const route = getRoute();
  updateNav();
  const content = $("#content");
  content.innerHTML = '<div class="loading">Loading…</div>';

  switch (route.view) {
    case "dashboard": await renderDashboard(content); break;
    case "cases": await renderCaseList(content); break;
    case "case-detail": await renderCaseDetail(content, route.id); break;
    case "analytics": await renderAnalytics(content); break;
    default: await renderDashboard(content);
  }
}

// ── Dashboard View ─────────────────────────────────────────────────────────
async function renderDashboard(container) {
  const stats = await ApiClient.getIncidentStats();

  const openCount = stats.by_status?.OPEN || 0;
  const approvedCount = stats.by_status?.APPROVED || 0;
  const rejectedCount = stats.by_status?.REJECTED || 0;
  const escalatedCount = stats.by_status?.ESCALATED || 0;

  container.innerHTML = `
    <div class="page-header">
      <h2>Dashboard</h2>
      <p>Real-time overview of traffic violation cases</p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card kpi-total">
        <div class="kpi-label">Total Cases</div>
        <div class="kpi-value">${stats.total || 0}</div>
        <div class="kpi-sub">All time</div>
      </div>
      <div class="kpi-card kpi-open">
        <div class="kpi-label">Pending Review</div>
        <div class="kpi-value">${openCount}</div>
        <div class="kpi-sub">Awaiting decision</div>
      </div>
      <div class="kpi-card kpi-approved">
        <div class="kpi-label">Approved</div>
        <div class="kpi-value">${approvedCount}</div>
        <div class="kpi-sub">Challans issued</div>
      </div>
      <div class="kpi-card kpi-rejected">
        <div class="kpi-label">Rejected</div>
        <div class="kpi-value">${rejectedCount}</div>
        <div class="kpi-sub">False positives</div>
      </div>
      <div class="kpi-card kpi-escalated">
        <div class="kpi-label">Escalated</div>
        <div class="kpi-value">${escalatedCount}</div>
        <div class="kpi-sub">Needs admin review</div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>Violation Trend</h3>
        <canvas id="dashTrendChart" height="260"></canvas>
      </div>
      <div class="chart-card">
        <h3>Violations by Type</h3>
        <canvas id="dashTypeChart" height="260"></canvas>
      </div>
      <div class="chart-card">
        <h3>Top Cameras</h3>
        <canvas id="dashCameraChart" height="260"></canvas>
      </div>
    </div>
  `;

  // Render charts
  if (stats.by_day && Object.keys(stats.by_day).length > 0)
    renderViolationTrendChart("dashTrendChart", stats.by_day);
  if (stats.by_violation_type && Object.keys(stats.by_violation_type).length > 0)
    renderViolationTypeChart("dashTypeChart", stats.by_violation_type);
  if (stats.by_camera && Object.keys(stats.by_camera).length > 0)
    renderCameraChart("dashCameraChart", stats.by_camera);
}

// ── Case List View ─────────────────────────────────────────────────────────
async function renderCaseList(container) {
  const offset = (state.currentPage - 1) * state.pageSize;

  const data = await ApiClient.getIncidents({
    ...state.filters,
    limit: state.pageSize,
    offset,
    sort_by: state.sortBy,
    sort_dir: state.sortDir,
  });

  const incidents = data.incidents || [];
  const total = data.total || 0;
  const totalPages = Math.ceil(total / state.pageSize) || 1;

  container.innerHTML = `
    <div class="page-header">
      <h2>Cases</h2>
      <p>Review and manage traffic violation incidents</p>
    </div>

    <!-- Filters -->
    <div class="filters-bar" id="filtersBar">
      <label>Status</label>
      <select id="filterStatus">
        <option value="">All</option>
        <option value="OPEN">Open</option>
        <option value="APPROVED">Approved</option>
        <option value="REJECTED">Rejected</option>
        <option value="ESCALATED">Escalated</option>
      </select>

      <label>Violation</label>
      <select id="filterViolation">
        <option value="">All</option>
        <option value="NO_HELMET">No Helmet</option>
        <option value="TRIPLE_RIDING">Triple Riding</option>
      </select>

      <label>Camera</label>
      <input type="text" id="filterCamera" placeholder="cam-..." style="width:120px">

      <label>Plate</label>
      <input type="text" id="filterPlate" placeholder="MH12..." style="width:100px">

      <label>From</label>
      <input type="date" id="filterDateFrom">

      <label>To</label>
      <input type="date" id="filterDateTo">

      <button class="btn btn-primary btn-sm" id="btnApplyFilters">Apply</button>
      <button class="btn btn-ghost btn-sm" id="btnClearFilters">Clear</button>
    </div>

    <!-- Table -->
    <div class="data-table-wrap">
      <table class="data-table" id="caseTable">
        <thead>
          <tr>
            <th data-sort="incident_id">ID <span class="sort-arrow">↕</span></th>
            <th data-sort="timestamp">Date <span class="sort-arrow">↕</span></th>
            <th data-sort="camera_id">Camera <span class="sort-arrow">↕</span></th>
            <th data-sort="primary_violation">Violation <span class="sort-arrow">↕</span></th>
            <th data-sort="status">Status <span class="sort-arrow">↕</span></th>
            <th>Plate</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="caseTableBody"></tbody>
      </table>
      <div class="pagination" id="pagination"></div>
    </div>
  `;

  // Populate table rows
  const tbody = $("#caseTableBody");
  if (incidents.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="empty-state"><div class="empty-icon">📋</div>No cases found matching your filters.</td></tr>';
  } else {
    incidents.forEach(inc => {
      const plate = inc.violations?.[0]?.plate_text || inc.plate_text || "—";
      const tr = el("tr", { className: "clickable" });
      tr.innerHTML = `
        <td style="font-family:monospace;font-size:0.78rem;">${inc.incident_id}</td>
        <td>${formatDate(inc.timestamp || inc.created_at)}</td>
        <td>${inc.camera_id || "—"}</td>
        <td>${inc.primary_violation || "—"}</td>
        <td>${statusBadge(inc.status)}</td>
        <td style="font-family:monospace;">${plate}</td>
        <td>
          <button class="btn btn-ghost btn-sm" data-action="view" data-id="${inc.incident_id}">View</button>
          ${inc.status === "OPEN" ? `
            <button class="btn btn-approve btn-sm" data-action="quick-approve" data-id="${inc.incident_id}">✓</button>
            <button class="btn btn-reject btn-sm" data-action="quick-reject" data-id="${inc.incident_id}">✗</button>
          ` : ""}
        </td>
      `;
      // Row click → detail (but not on buttons)
      tr.addEventListener("click", (e) => {
        if (e.target.closest("button")) return;
        navigate(`#case/${inc.incident_id}`);
      });
      tbody.appendChild(tr);
    });
  }

  // Pagination
  const pag = $("#pagination");
  pag.innerHTML = `
    <span class="page-info">Showing ${offset + 1}–${Math.min(offset + state.pageSize, total)} of ${total} cases</span>
    <div class="page-buttons">
      <button class="btn btn-ghost btn-sm" id="btnPrevPage" ${state.currentPage <= 1 ? "disabled" : ""}>← Prev</button>
      <span style="padding:4px 12px;font-size:0.8rem;color:#a1a1aa;">Page ${state.currentPage} / ${totalPages}</span>
      <button class="btn btn-ghost btn-sm" id="btnNextPage" ${state.currentPage >= totalPages ? "disabled" : ""}>Next →</button>
    </div>
  `;

  // ── Event Bindings ──
  // Restore filter values
  if (state.filters.status) $("#filterStatus").value = state.filters.status;
  if (state.filters.violation_type) $("#filterViolation").value = state.filters.violation_type;
  if (state.filters.camera_id) $("#filterCamera").value = state.filters.camera_id;
  if (state.filters.plate) $("#filterPlate").value = state.filters.plate;
  if (state.filters.start_date) $("#filterDateFrom").value = state.filters.start_date;
  if (state.filters.end_date) $("#filterDateTo").value = state.filters.end_date;

  // Apply filters
  $("#btnApplyFilters").addEventListener("click", () => {
    state.filters = {
      status: $("#filterStatus").value || undefined,
      violation_type: $("#filterViolation").value || undefined,
      camera_id: $("#filterCamera").value || undefined,
      plate: $("#filterPlate").value || undefined,
      start_date: $("#filterDateFrom").value || undefined,
      end_date: $("#filterDateTo").value || undefined,
    };
    state.currentPage = 1;
    renderCaseList(container);
  });

  // Clear filters
  $("#btnClearFilters").addEventListener("click", () => {
    state.filters = {};
    state.currentPage = 1;
    renderCaseList(container);
  });

  // Pagination
  const prevBtn = $("#btnPrevPage");
  const nextBtn = $("#btnNextPage");
  if (prevBtn) prevBtn.addEventListener("click", () => { state.currentPage--; renderCaseList(container); });
  if (nextBtn) nextBtn.addEventListener("click", () => { state.currentPage++; renderCaseList(container); });

  // Sort headers
  $$("#caseTable th[data-sort]").forEach(th => {
    th.addEventListener("click", () => {
      const field = th.dataset.sort;
      if (state.sortBy === field) {
        state.sortDir = state.sortDir === "desc" ? "asc" : "desc";
      } else {
        state.sortBy = field;
        state.sortDir = "desc";
      }
      renderCaseList(container);
    });
    // Highlight active sort
    const arrow = th.querySelector(".sort-arrow");
    if (th.dataset.sort === state.sortBy) {
      arrow.classList.add("active");
      arrow.textContent = state.sortDir === "desc" ? "↓" : "↑";
    }
  });

  // Quick action buttons
  tbody.addEventListener("click", async (e) => {
    const btn = e.target.closest("button[data-action]");
    if (!btn) return;
    e.stopPropagation();
    const { action, id } = btn.dataset;

    if (action === "view") {
      navigate(`#case/${id}`);
    } else if (action === "quick-approve") {
      await ApiClient.submitReview(id, "APPROVE", "Quick approve from case list");
      showToast(`Case ${id} approved`, "success");
      renderCaseList(container);
    } else if (action === "quick-reject") {
      await ApiClient.submitReview(id, "REJECT", "Quick reject from case list");
      showToast(`Case ${id} rejected`, "info");
      renderCaseList(container);
    }
  });
}

// ── Case Detail View ───────────────────────────────────────────────────────
async function renderCaseDetail(container, incidentId) {
  const detail = await ApiClient.getIncidentDetail(incidentId);

  if (!detail) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        <p>Incident <strong>${incidentId}</strong> not found.</p>
        <button class="btn btn-ghost" onclick="navigate('#cases')">← Back to Cases</button>
      </div>`;
    return;
  }

  const viol = detail.violations?.[0] || {};
  const plate = viol.plate_text || detail.plate_text || "—";
  const plateConf = viol.plate_confidence;
  const violConf = viol.confidence;
  const violType = viol.violation_type || detail.primary_violation || "—";
  const reviews = detail.reviews || [];

  // Build reviewer history HTML
  let historyHtml = "";
  if (reviews.length === 0) {
    historyHtml = '<p class="timeline-empty">No review actions yet.</p>';
  } else {
    historyHtml = reviews.map(r => `
      <div class="timeline-item">
        <div class="tl-time">${formatDate(r.created_at)}</div>
        <div class="tl-body">
          <div class="tl-action">${r.reviewer_id} → ${statusBadge(r.action)}</div>
          ${r.notes ? `<div class="tl-notes">"${r.notes}"</div>` : ""}
        </div>
      </div>
    `).join("");
  }

  // Evidence image — mock placeholder if no real assets
  const evidenceUrl = (detail.evidence_assets && detail.evidence_assets.length > 0)
    ? detail.evidence_assets[0]
    : `https://placehold.co/800x420/1a1a2e/6366f1?text=Evidence+${incidentId}&font=inter`;

  container.innerHTML = `
    <div class="detail-back">
      <button class="btn btn-ghost" id="btnBackToList">← Back to Cases</button>
    </div>

    <div class="page-header">
      <h2>Case: ${incidentId}</h2>
      <p>${statusBadge(detail.status)} &nbsp; ${formatDate(detail.timestamp || detail.created_at)}</p>
    </div>

    <div class="detail-grid">
      <!-- Evidence Image -->
      <div class="detail-evidence">
        <img src="${evidenceUrl}" alt="Evidence for ${incidentId}" id="evidenceImg">
      </div>

      <!-- Metadata -->
      <div class="detail-meta">
        <div class="meta-row">
          <span class="meta-label">Violation Type</span>
          <span class="meta-value">${violType}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Detection Confidence</span>
          <span class="meta-value">${confidenceBar(violConf)}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">License Plate</span>
          <span class="meta-value" style="font-family:monospace;font-size:1.05rem;">${plate}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Plate Confidence</span>
          <span class="meta-value">${confidenceBar(plateConf)}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Camera ID</span>
          <span class="meta-value">${detail.camera_id || "—"}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Zone</span>
          <span class="meta-value">${detail.zone || "—"}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Timestamp</span>
          <span class="meta-value">${formatDate(detail.timestamp || detail.created_at)}</span>
        </div>
        <div class="meta-row">
          <span class="meta-label">Current Status</span>
          <span class="meta-value">${statusBadge(detail.status)}</span>
        </div>
      </div>
    </div>

    <!-- Reviewer History -->
    <div class="review-history">
      <h3>📋 Review History</h3>
      ${historyHtml}
    </div>

    <!-- Decision Form -->
    <div class="decision-form" id="decisionForm">
      <h3>⚖️ Make Decision</h3>
      <textarea id="decisionNotes" placeholder="Optional reviewer comments…"></textarea>
      <div class="decision-buttons">
        <button class="btn btn-approve" data-decision="APPROVE">✓ Approve (Issue Challan)</button>
        <button class="btn btn-reject" data-decision="REJECT">✗ Reject (False Positive)</button>
        <button class="btn btn-escalate" data-decision="ESCALATE">⚠ Escalate (Needs Admin)</button>
      </div>
    </div>
  `;

  // ── Event Bindings ──
  $("#btnBackToList").addEventListener("click", () => navigate("#cases"));

  $$("#decisionForm button[data-decision]").forEach(btn => {
    btn.addEventListener("click", async () => {
      const action = btn.dataset.decision;
      const notes = $("#decisionNotes").value;
      btn.disabled = true;
      btn.textContent = "Submitting…";

      try {
        const result = await ApiClient.submitReview(incidentId, action, notes);
        const newStatus = result?.data?.new_status || action;
        showToast(`Case ${incidentId} marked as ${newStatus}`, "success");
        // Reload detail to show updated status + review history
        setTimeout(() => renderCaseDetail(container, incidentId), 800);
      } catch (err) {
        showToast("Error submitting decision", "error");
        btn.disabled = false;
        btn.textContent = btn.dataset.decision;
      }
    });
  });
}

// ── Analytics View ─────────────────────────────────────────────────────────
async function renderAnalytics(container) {
  container.innerHTML = `
    <div class="page-header">
      <h2>Analytics</h2>
      <p>Visualize violation patterns and trends</p>
    </div>

    <!-- Analytics Filters -->
    <div class="filters-bar" id="analyticsFilters">
      <label>From</label>
      <input type="date" id="analyticsDateFrom">
      <label>To</label>
      <input type="date" id="analyticsDateTo">
      <label>Camera</label>
      <input type="text" id="analyticsCameraFilter" placeholder="cam-..." style="width:120px">
      <label>Violation</label>
      <select id="analyticsViolationFilter">
        <option value="">All</option>
        <option value="NO_HELMET">No Helmet</option>
        <option value="TRIPLE_RIDING">Triple Riding</option>
      </select>
      <button class="btn btn-primary btn-sm" id="btnRefreshAnalytics">Refresh</button>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>📈 Violation Trend Over Time</h3>
        <canvas id="analyticsTrendChart" height="280"></canvas>
      </div>
      <div class="chart-card">
        <h3>🍩 Violations by Type</h3>
        <canvas id="analyticsTypeChart" height="280"></canvas>
      </div>
      <div class="chart-card">
        <h3>📊 Violations by Camera</h3>
        <canvas id="analyticsCameraChart" height="280"></canvas>
      </div>
      <div class="chart-card">
        <h3>📋 Status Distribution</h3>
        <canvas id="analyticsStatusChart" height="280"></canvas>
      </div>
    </div>
  `;

  async function loadAnalytics() {
    const summary = await ApiClient.getAnalyticsSummary();

    if (summary.by_day && Object.keys(summary.by_day).length > 0) {
      renderViolationTrendChart("analyticsTrendChart", summary.by_day);
    } else if (summary.by_violation_type) {
      // Fallback: use stats endpoint which always has by_day
      const stats = await ApiClient.getIncidentStats();
      if (stats.by_day) renderViolationTrendChart("analyticsTrendChart", stats.by_day);
    }

    if (summary.by_violation_type && Object.keys(summary.by_violation_type).length > 0)
      renderViolationTypeChart("analyticsTypeChart", summary.by_violation_type);

    if (summary.by_camera || summary.top_cameras) {
      const camData = summary.by_camera || summary.top_cameras;
      if (Object.keys(camData).length > 0) renderCameraChart("analyticsCameraChart", camData);
    }

    if (summary.by_status && Object.keys(summary.by_status).length > 0)
      renderStatusChart("analyticsStatusChart", summary.by_status);
  }

  await loadAnalytics();

  // Refresh button
  $("#btnRefreshAnalytics").addEventListener("click", loadAnalytics);
}

// ── Initialization ─────────────────────────────────────────────────────────
window.addEventListener("hashchange", routeToView);
window.addEventListener("DOMContentLoaded", () => {
  if (!window.location.hash) window.location.hash = "#dashboard";
  routeToView();
});
