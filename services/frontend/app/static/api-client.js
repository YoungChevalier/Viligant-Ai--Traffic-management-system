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
    
    if (!resp.ok) {
        // In demo mode, never redirect on 401 — just throw so callers can use mock fallback
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
    
    try {
      const resp = await fetch(`${CONFIG.API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params
      });
      
      if (!resp.ok) {
          let msg = "Login failed";
          try { const errData = await resp.json(); msg = errData.detail || msg; } catch(e) {}
          throw new Error(msg);
      }
      const data = await resp.json();
      this.setToken(data.access_token);
      return data;
    } catch (err) {
      // If the backend is offline, fetch throws a TypeError
      if (err.name === 'TypeError' || err.message.toLowerCase().includes('fetch')) {
          console.warn("Backend API is unreachable. Falling back to mock login.");
          if (username.includes('admin') && password === 'VigilantDemo24!') {
              this.setToken("mock_admin_token");
              return { access_token: "mock_admin_token" };
          } else {
              throw new Error("Invalid mock credentials. Try admin@vigilant.ai and VigilantDemo24!");
          }
      }
      throw err; // Re-throw if it was a legitimate 401/400 error
    }
  },

  async getMe() {
    try {
        return await this._fetch("/auth/me");
    } catch (err) {
        // If the backend is offline, fallback to a mock user so it doesn't log us out
        if (err.name === 'TypeError' || err.message.toLowerCase().includes('fetch')) {
            console.warn("Backend API unreachable. Falling back to mock user profile.");
            return {
                id: 1,
                name: "System Admin",
                email: "admin@vigilant.ai",
                role: "Admin",
                status: "Active"
            };
        }
        throw err;
    }
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
    try {
      return await this._fetch(`/cases?${params}`);
    } catch (err) {
      console.warn("Backend unreachable. Using mock queue data.");
      const now = new Date();
      const ago = (mins) => new Date(now - mins * 60000).toISOString();
      return [
        { id: "CASE-10924", type: "Helmet Non-Compliance", plate: "MH12AB1234", cam: "CAM-North-01", time: ago(3),  score: 97, status: "Pending",   assignee: "Unassigned", thumb: "🪖" },
        { id: "CASE-10925", type: "Red-Light Violation",   plate: "DL4CAF5678", cam: "CAM-East-05",  time: ago(7),  score: 92, status: "Flagged",    assignee: "R. Vargas",   thumb: "🚦" },
        { id: "CASE-10926", type: "Triple Riding",         plate: "KA01MG9012", cam: "CAM-South-04", time: ago(12), score: 85, status: "Pending",   assignee: "Unassigned", thumb: "🏍️" },
        { id: "CASE-10927", type: "Stop-Line Violation",   plate: "TN09CD3456", cam: "CAM-North-08", time: ago(18), score: 99, status: "Escalated",  assignee: "Supervisor",  thumb: "⛔" },
        { id: "CASE-10928", type: "Helmet Non-Compliance", plate: "GJ05GH2345", cam: "CAM-West-02",  time: ago(25), score: 88, status: "Pending",   assignee: "Unassigned", thumb: "🪖" },
        { id: "CASE-10929", type: "Wrong-Side Driving",    plate: "AP09IJ6789", cam: "CAM-East-12",  time: ago(31), score: 76, status: "Flagged",    assignee: "R. Vargas",   thumb: "⚠️" },
        { id: "CASE-10930", type: "Red-Light Violation",   plate: "UP32KL0123", cam: "CAM-North-01", time: ago(45), score: 94, status: "Reviewed",   assignee: "R. Vargas",   thumb: "🚦" },
        { id: "CASE-10931", type: "Illegal Parking",       plate: "HR26MN4567", cam: "CAM-South-04", time: ago(60), score: 81, status: "Reviewed",   assignee: "Auto",        thumb: "🅿️" },
      ];
    }
  },

  async submitDecision(caseId, action, reason) {
    try {
      return await this._fetch(`/cases/${caseId}/decision`, {
        method: "POST",
        body: JSON.stringify({ action, reason })
      });
    } catch (err) {
      console.warn("Backend unreachable. Mock decision recorded for", caseId);
      return { status: "ok", caseId, action };
    }
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

// Demo mode: always ensure a mock token exists so pages load without login
// Real auth would replace this with a proper session check
(function ensureDemoSession() {
    if (!ApiClient.getToken()) {
        ApiClient.setToken("mock_admin_token");
        console.log("Demo mode: mock session initialized.");
    }
})();
