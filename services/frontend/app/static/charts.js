/**
 * charts.js
 * Chart rendering utilities for the Traffic Violation Dashboard.
 * Depends on Chart.js loaded via CDN in index.html.
 *
 * Each function accepts a canvas element ID and data object,
 * destroys any previous chart on that canvas, and renders a new one.
 */

// ── Chart Instance Registry ────────────────────────────────────────────────
const _chartInstances = {};

function _destroyIfExists(canvasId) {
  if (_chartInstances[canvasId]) {
    _chartInstances[canvasId].destroy();
    delete _chartInstances[canvasId];
  }
}

// ── Theme Colors ───────────────────────────────────────────────────────────
const CHART_COLORS = {
  indigo:     "#6366f1",
  indigoFade: "rgba(99, 102, 241, 0.15)",
  green:      "#22c55e",
  greenFade:  "rgba(34, 197, 94, 0.15)",
  red:        "#ef4444",
  redFade:    "rgba(239, 68, 68, 0.15)",
  amber:      "#f59e0b",
  amberFade:  "rgba(245, 158, 11, 0.15)",
  blue:       "#3b82f6",
  blueFade:   "rgba(59, 130, 246, 0.15)",
  cyan:       "#06b6d4",
  cyanFade:   "rgba(6, 182, 212, 0.15)",
  pink:       "#ec4899",
  pinkFade:   "rgba(236, 72, 153, 0.15)",
  slate:      "#94a3b8",
  slateFade:  "rgba(148, 163, 184, 0.15)",
};

const PALETTE = [
  CHART_COLORS.indigo,
  CHART_COLORS.green,
  CHART_COLORS.amber,
  CHART_COLORS.red,
  CHART_COLORS.blue,
  CHART_COLORS.cyan,
  CHART_COLORS.pink,
  CHART_COLORS.slate,
];

const PALETTE_FADE = [
  CHART_COLORS.indigoFade,
  CHART_COLORS.greenFade,
  CHART_COLORS.amberFade,
  CHART_COLORS.redFade,
  CHART_COLORS.blueFade,
  CHART_COLORS.cyanFade,
  CHART_COLORS.pinkFade,
  CHART_COLORS.slateFade,
];

// ── Common Chart.js defaults ───────────────────────────────────────────────
const COMMON_OPTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: "#a1a1aa",
        font: { family: "'Inter', sans-serif", size: 11 },
        padding: 16,
        usePointStyle: true,
        pointStyleWidth: 10,
      },
    },
    tooltip: {
      backgroundColor: "rgba(22, 24, 34, 0.95)",
      titleColor: "#fafafa",
      bodyColor: "#e4e4e7",
      borderColor: "rgba(255,255,255,0.08)",
      borderWidth: 1,
      cornerRadius: 6,
      padding: 10,
      titleFont: { family: "'Inter', sans-serif", weight: "600" },
      bodyFont: { family: "'Inter', sans-serif" },
    },
  },
};

const SCALE_OPTS = {
  x: {
    ticks: { color: "#71717a", font: { family: "'Inter', sans-serif", size: 11 } },
    grid: { color: "rgba(255,255,255,0.04)" },
    border: { color: "rgba(255,255,255,0.08)" },
  },
  y: {
    beginAtZero: true,
    ticks: { color: "#71717a", font: { family: "'Inter', sans-serif", size: 11 }, precision: 0 },
    grid: { color: "rgba(255,255,255,0.04)" },
    border: { color: "rgba(255,255,255,0.08)" },
  },
};

// ── Public Chart Functions ─────────────────────────────────────────────────

/**
 * Doughnut chart — Violation count by type.
 * @param {string} canvasId
 * @param {Object} data — { "NO_HELMET": 30, "TRIPLE_RIDING": 12 }
 */
function renderViolationTypeChart(canvasId, data) {
  _destroyIfExists(canvasId);
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const labels = Object.keys(data);
  const values = Object.values(data);

  _chartInstances[canvasId] = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: PALETTE.slice(0, labels.length),
        borderColor: "transparent",
        borderWidth: 0,
        hoverOffset: 8,
      }],
    },
    options: {
      ...COMMON_OPTS,
      cutout: "65%",
      plugins: {
        ...COMMON_OPTS.plugins,
        legend: {
          ...COMMON_OPTS.plugins.legend,
          position: "bottom",
        },
      },
    },
  });
}

/**
 * Line chart with gradient fill — Violations over time (by day).
 * @param {string} canvasId
 * @param {Object} data — { "2026-06-15": 8, "2026-06-16": 12 }
 */
function renderViolationTrendChart(canvasId, data) {
  _destroyIfExists(canvasId);
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height || 280);
  gradient.addColorStop(0, "rgba(99, 102, 241, 0.35)");
  gradient.addColorStop(1, "rgba(99, 102, 241, 0.0)");

  const labels = Object.keys(data);
  const values = Object.values(data);

  _chartInstances[canvasId] = new Chart(canvas, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Violations",
        data: values,
        borderColor: CHART_COLORS.indigo,
        backgroundColor: gradient,
        fill: true,
        tension: 0.35,
        pointRadius: 4,
        pointBackgroundColor: CHART_COLORS.indigo,
        pointBorderColor: "#161822",
        pointBorderWidth: 2,
        pointHoverRadius: 7,
      }],
    },
    options: {
      ...COMMON_OPTS,
      scales: SCALE_OPTS,
      plugins: {
        ...COMMON_OPTS.plugins,
        legend: { display: false },
      },
    },
  });
}

/**
 * Horizontal bar chart — Top cameras or locations by violation count.
 * @param {string} canvasId
 * @param {Object} data — { "cam-01": 18, "cam-02": 14 }
 */
function renderCameraChart(canvasId, data) {
  _destroyIfExists(canvasId);
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const labels = Object.keys(data);
  const values = Object.values(data);

  _chartInstances[canvasId] = new Chart(canvas, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Violations",
        data: values,
        backgroundColor: PALETTE.slice(0, labels.length).map((c, i) => PALETTE_FADE[i]),
        borderColor: PALETTE.slice(0, labels.length),
        borderWidth: 1,
        borderRadius: 4,
        barPercentage: 0.7,
      }],
    },
    options: {
      ...COMMON_OPTS,
      indexAxis: "y",
      scales: {
        x: {
          ...SCALE_OPTS.x,
          beginAtZero: true,
          ticks: { ...SCALE_OPTS.x.ticks, precision: 0 },
        },
        y: {
          ...SCALE_OPTS.y,
          grid: { display: false },
          ticks: { ...SCALE_OPTS.y.ticks, color: "#a1a1aa" },
        },
      },
      plugins: {
        ...COMMON_OPTS.plugins,
        legend: { display: false },
      },
    },
  });
}

/**
 * Status distribution chart — Doughnut showing OPEN/APPROVED/REJECTED/ESCALATED.
 * Uses fixed colors per status.
 * @param {string} canvasId
 * @param {Object} data — { "OPEN": 15, "APPROVED": 20, ... }
 */
function renderStatusChart(canvasId, data) {
  _destroyIfExists(canvasId);
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const STATUS_COLORS = {
    OPEN:      CHART_COLORS.blue,
    APPROVED:  CHART_COLORS.green,
    REJECTED:  CHART_COLORS.red,
    ESCALATED: CHART_COLORS.amber,
  };

  const labels = Object.keys(data);
  const values = Object.values(data);
  const colors = labels.map(l => STATUS_COLORS[l] || CHART_COLORS.slate);

  _chartInstances[canvasId] = new Chart(canvas, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderColor: "transparent",
        borderWidth: 0,
        hoverOffset: 8,
      }],
    },
    options: {
      ...COMMON_OPTS,
      cutout: "65%",
      plugins: {
        ...COMMON_OPTS.plugins,
        legend: {
          ...COMMON_OPTS.plugins.legend,
          position: "bottom",
        },
      },
    },
  });
}
