/**
 * api-client.js
 * API abstraction layer for the Traffic Violation Reviewer Dashboard.
 *
 * Tries real backend endpoints first. On network failure, falls back to
 * realistic mock data so the UI is always functional for development.
 */

// ── Configuration ──────────────────────────────────────────────────────────
const CONFIG = {
  USE_MOCKS: false, // Set to false to allow Playwright to intercept real fetch calls
  DASHBOARD_API: "/api/v1",
  REVIEW_API: "/api/v1",
  ANALYTICS_API: "/api/v1",
  REVIEWER_ID: "rev_operator_01"
};

// ── Mock Data ──────────────────────────────────────────────────────────────

const MOCK_CAMERAS = ["cam-northex-01", "cam-southex-02", "cam-east-03", "cam-west-04", "cam-central-05"];
const MOCK_VIOLATIONS = ["NO_HELMET", "NO_HELMET", "NO_HELMET", "TRIPLE_RIDING"];
const MOCK_STATUSES = ["OPEN", "OPEN", "OPEN", "APPROVED", "REJECTED", "ESCALATED"];
const MOCK_PLATES = ["MH12AB1234", "DL4CAF5678", "KA01MG9012", "TN09CD3456", "RJ14EF7890",
                      "GJ05GH2345", "AP09IJ6789", "UP32KL0123", "HR26MN4567", null];

function _mockId(i) { return `INC-2026-${String(i).padStart(5, "0")}`; }
function _mockDate(daysAgo) {
  const d = new Date();
  d.setDate(d.getDate() - daysAgo);
  return d.toISOString();
}

function _generateMockIncidents() {
  const incidents = [];
  for (let i = 1; i <= 18; i++) {
    const daysAgo = Math.floor(Math.random() * 7);
    incidents.push({
      incident_id: _mockId(i),
      timestamp: _mockDate(daysAgo),
      created_at: _mockDate(daysAgo),
      camera_id: MOCK_CAMERAS[i % MOCK_CAMERAS.length],
      primary_violation: MOCK_VIOLATIONS[i % MOCK_VIOLATIONS.length],
      status: MOCK_STATUSES[i % MOCK_STATUSES.length],
      zone: ["North", "South", "East", "West", "Central"][i % 5],
      violations: [{
        violation_type: MOCK_VIOLATIONS[i % MOCK_VIOLATIONS.length],
        confidence: +(0.75 + Math.random() * 0.24).toFixed(2),
        plate_text: MOCK_PLATES[i % MOCK_PLATES.length],
        plate_confidence: MOCK_PLATES[i % MOCK_PLATES.length] ? +(0.80 + Math.random() * 0.19).toFixed(2) : null,
      }],
      evidence_assets: [],
      reviews: i % 3 === 0 ? [{
        reviewer_id: "rev_admin_02",
        action: "ESCALATE",
        notes: "Needs additional verification — image partially occluded.",
        created_at: _mockDate(daysAgo > 0 ? daysAgo - 1 : 0),
      }] : [],
    });
  }
  return incidents;
}

let _mockIncidents = null;
function _getMockIncidents() {
  if (!_mockIncidents) _mockIncidents = _generateMockIncidents();
  return _mockIncidents;
}

function _buildMockStats() {
  const incs = _getMockIncidents();
  const byStatus = {}, byViolation = {}, byCamera = {}, byDay = {};
  incs.forEach(inc => {
    byStatus[inc.status] = (byStatus[inc.status] || 0) + 1;
    byViolation[inc.primary_violation] = (byViolation[inc.primary_violation] || 0) + 1;
    byCamera[inc.camera_id] = (byCamera[inc.camera_id] || 0) + 1;
    const day = inc.timestamp.slice(0, 10);
    byDay[day] = (byDay[day] || 0) + 1;
  });
  return { total: incs.length, by_status: byStatus, by_violation_type: byViolation, by_camera: byCamera, by_day: byDay };
}

// ── Fetch Wrapper ──────────────────────────────────────────────────────────

async function _apiFetch(baseUrl, path, options = {}) {
  const url = `${baseUrl}${path}`;
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  return resp.json();
}

// ── Public API Client ──────────────────────────────────────────────────────

const ApiClient = {

  /**
   * GET /incidents/stats — Dashboard KPIs.
   */
  async getIncidentStats() {
    if (CONFIG.USE_MOCKS) return _buildMockStats();
    try {
      return await _apiFetch(CONFIG.DASHBOARD_API, "/incidents/stats");
    } catch (e) {
      console.warn("[ApiClient] getIncidentStats failed, using mocks:", e.message);
      return _buildMockStats();
    }
  },

  /**
   * GET /incidents?status=...&violation_type=...&limit=...&offset=...
   * Filterable, paginated incident list.
   */
  async getIncidents({ status, violation_type, camera_id, plate, start_date, end_date, limit = 10, offset = 0, sort_by, sort_dir } = {}) {
    if (CONFIG.USE_MOCKS) return this._mockGetIncidents({ status, violation_type, camera_id, plate, start_date, end_date, limit, offset, sort_by, sort_dir });
    try {
      const params = new URLSearchParams();
      if (status) params.set("status", status);
      if (violation_type) params.set("violation_type", violation_type);
      params.set("limit", limit);
      params.set("offset", offset);
      return await _apiFetch(CONFIG.DASHBOARD_API, `/incidents?${params}`);
    } catch (e) {
      console.error("[ApiClient] getIncidents failed:", e);
      throw e;
    }
  },

  /**
   * GET /incidents/:id — Full incident detail.
   */
  async getIncidentDetail(incidentId) {
    if (CONFIG.USE_MOCKS) return this._mockGetIncidentDetail(incidentId);
    try {
      return await _apiFetch(CONFIG.DASHBOARD_API, `/incidents/${incidentId}`);
    } catch (e) {
      console.warn("[ApiClient] getIncidentDetail failed, using mocks:", e.message);
      return this._mockGetIncidentDetail(incidentId);
    }
  },

  /**
   * POST /incidents/:id/review — Submit review decision.
   */
  async submitReview(incidentId, action, notes) {
    const payload = { reviewer_id: CONFIG.REVIEWER_ID, action, notes: notes || null };
    if (CONFIG.USE_MOCKS) return this._mockSubmitReview(incidentId, action);
    try {
      return await _apiFetch(CONFIG.DASHBOARD_API, `/incidents/${incidentId}/review`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
    } catch (e) {
      console.warn("[ApiClient] submitReview failed, using mocks:", e.message);
      return this._mockSubmitReview(incidentId, action);
    }
  },

  /**
   * GET /analytics/summary — Analytics aggregation.
   */
  async getAnalyticsSummary() {
    if (CONFIG.USE_MOCKS) return _buildMockStats();
    try {
      return await _apiFetch(CONFIG.ANALYTICS_API, "/analytics/summary");
    } catch (e) {
      console.warn("[ApiClient] getAnalyticsSummary failed, using mocks:", e.message);
      return _buildMockStats();
    }
  },

  /**
   * GET /analytics/cases?plate=...&violation_type=... — Searchable analytics records.
   */
  async searchAnalyticsCases(filters = {}) {
    if (CONFIG.USE_MOCKS) return this._mockGetIncidents(filters);
    try {
      const params = new URLSearchParams();
      for (const [k, v] of Object.entries(filters)) {
        if (v !== undefined && v !== null && v !== "") params.set(k, v);
      }
      return await _apiFetch(CONFIG.ANALYTICS_API, `/analytics/cases?${params}`);
    } catch (e) {
      console.warn("[ApiClient] searchAnalyticsCases failed, using mocks:", e.message);
      return this._mockGetIncidents(filters);
    }
  },

  // ── Mock Implementations ──────────────────────────────────────────────

  _mockGetIncidents({ status, violation_type, camera_id, plate, start_date, end_date, limit = 10, offset = 0, sort_by, sort_dir } = {}) {
    let results = [..._getMockIncidents()];
    if (status) results = results.filter(r => r.status === status);
    if (violation_type) results = results.filter(r => r.primary_violation === violation_type);
    if (camera_id) results = results.filter(r => r.camera_id === camera_id);
    if (plate) results = results.filter(r => (r.violations[0]?.plate_text || "").toUpperCase().includes(plate.toUpperCase()));
    if (start_date) results = results.filter(r => r.timestamp >= start_date);
    if (end_date) results = results.filter(r => r.timestamp <= end_date + "T23:59:59Z");

    // Sort
    const dir = sort_dir === "asc" ? 1 : -1;
    if (sort_by === "timestamp") results.sort((a, b) => a.timestamp.localeCompare(b.timestamp) * dir);
    else if (sort_by === "camera_id") results.sort((a, b) => a.camera_id.localeCompare(b.camera_id) * dir);
    else if (sort_by === "status") results.sort((a, b) => a.status.localeCompare(b.status) * dir);
    else if (sort_by === "primary_violation") results.sort((a, b) => a.primary_violation.localeCompare(b.primary_violation) * dir);
    else results.sort((a, b) => b.timestamp.localeCompare(a.timestamp)); // default: newest first

    const total = results.length;
    const page = results.slice(offset, offset + limit);
    return { total, limit, offset, incidents: page };
  },

  _mockGetIncidentDetail(incidentId) {
    const inc = _getMockIncidents().find(i => i.incident_id === incidentId);
    if (!inc) return null;
    return { ...inc };
  },

  _mockSubmitReview(incidentId, action) {
    const statusMap = { APPROVE: "APPROVED", REJECT: "REJECTED", ESCALATE: "ESCALATED" };
    const newStatus = statusMap[action] || "OPEN";

    // Update mock store
    const inc = _getMockIncidents().find(i => i.incident_id === incidentId);
    if (inc) {
      inc.status = newStatus;
      inc.reviews.push({
        reviewer_id: CONFIG.REVIEWER_ID,
        action,
        notes: "Mock review action",
        created_at: new Date().toISOString(),
      });
    }

    return { status: "success", data: { incident_id: incidentId, action, new_status: newStatus } };
  },
};
