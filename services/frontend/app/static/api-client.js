/**
 * api-client.js
 * Real API integration for Traffic Violation Reviewer Dashboard.
 */

const CONFIG = {
  API_BASE: window.location.hostname.includes("localhost") || window.location.hostname.includes("127.0.0.1") 
    ? "http://localhost:8000/api" 
    : "/api",
};

const ApiClient = {
  // Auth helpers
  getToken() {
    return localStorage.getItem("access_token");
  },
  
  setToken(token) {
    localStorage.setItem("access_token", token);
  },

  logout() {
    localStorage.removeItem("access_token");
    window.location.href = "./login.html";
  },

  async _fetch(path, options = {}) {
    const url = `${CONFIG.API_BASE}${path}`;
    const headers = {
      "Content-Type": "application/json",
      ...options.headers,
    };
    
    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const resp = await fetch(url, { ...options, headers });
    
    if (resp.status === 401 && !path.includes("/auth/login")) {
      this.logout();
      throw new Error("Unauthorized");
    }
    
    if (!resp.ok) {
        let msg = resp.statusText;
        try { const errData = await resp.json(); msg = errData.detail || msg; } catch(e) {}
        throw new Error(`HTTP ${resp.status}: ${msg}`);
    }
    return resp.json();
  },

  // Auth
  async login(username, password) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    
    const resp = await fetch(`${CONFIG.API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params
    });
    
    if (!resp.ok) {
        throw new Error("Login failed");
    }
    const data = await resp.json();
    this.setToken(data.access_token);
    return data;
  },

  async getMe() {
    return this._fetch("/auth/me");
  },

  // Dashboard
  async getDashboardSummary() {
    return this._fetch("/dashboard/summary");
  },

  // Cases / Queue
  async getQueue(filters = {}) {
    const params = new URLSearchParams();
    if (filters.status) params.set("status", filters.status);
    if (filters.violation_type) params.set("violation_type", filters.violation_type);
    return this._fetch(`/cases?${params}`);
  },

  async getCaseDetail(caseId) {
    return this._fetch(`/cases/${caseId}`);
  },

  async submitDecision(caseId, action, reason) {
    return this._fetch(`/cases/${caseId}/decision`, {
      method: "POST",
      body: JSON.stringify({ action, reason })
    });
  },

  // Others
  async getCameras() {
    return this._fetch("/cameras");
  },

  async getAlerts() {
    return this._fetch("/alerts");
  },

  async getSettings() {
    return this._fetch("/settings");
  }
};

// Check auth on page load (unless on login page)
if (!window.location.pathname.includes("login.html")) {
    if (!ApiClient.getToken()) {
        ApiClient.logout();
    } else {
        // Option to pre-fetch me if needed
        ApiClient.getMe().catch(() => ApiClient.logout());
    }
}
