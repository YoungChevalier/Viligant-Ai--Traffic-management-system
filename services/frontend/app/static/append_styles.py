import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Mock Dashboard Additional Styles
   ========================================================================== */

/* KPI Cards */
.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.kpi-trend {
    font-size: 0.8125rem;
    font-weight: 500;
}
.trend-up { color: var(--color-success); }
.trend-down { color: var(--color-danger); }
.trend-neutral { color: var(--color-text-muted); }

/* Detection Table Layout */
.detection-list-container {
    display: flex;
    flex-direction: column;
}
.detection-row {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    border-bottom: 1px solid var(--color-border);
    font-size: 0.875rem;
    transition: background-color 0.2s ease;
}
.detection-row:last-child {
    border-bottom: none;
}
.detection-row:hover:not(.header) {
    background-color: var(--color-bg-surface-hover);
    cursor: pointer;
}
.detection-row.header {
    background-color: var(--color-bg-base);
    font-weight: 600;
    color: var(--color-text-muted);
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding-top: 8px;
    padding-bottom: 8px;
}

.col-id { width: 15%; flex-shrink: 0; }
.col-type { width: 22%; flex-shrink: 0; }
.col-plate { width: 15%; flex-shrink: 0; }
.col-cam { width: 18%; flex-shrink: 0; }
.col-time { width: 12%; flex-shrink: 0; color: var(--color-text-muted); }
.col-score { width: 8%; flex-shrink: 0; }
.col-status { width: 10%; flex-shrink: 0; display: flex; justify-content: flex-end;}

.truncate {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Status Chips */
.status-chip {
    padding: 4px 8px;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
    white-space: nowrap;
}
.status-chip-success { background-color: rgba(34,197,94,0.1); color: var(--color-success); }
.status-chip-warning { background-color: rgba(245,158,11,0.1); color: var(--color-warning); }
.status-chip-danger { background-color: rgba(239,68,68,0.1); color: var(--color-danger); }

/* Alerts */
.alert-item {
    padding: 16px 20px;
    border-bottom: 1px solid var(--color-border);
}
.alert-item:last-child {
    border-bottom: none;
}
.alert-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}
.alert-title {
    font-weight: 600;
    font-size: 0.875rem;
}
.alert-time {
    font-size: 0.75rem;
    color: var(--color-text-muted);
}
.alert-desc {
    font-size: 0.8125rem;
    color: var(--color-text-muted);
}
.alert-info .alert-title { color: var(--color-primary); }
.alert-warning .alert-title { color: var(--color-warning); }
.alert-critical .alert-title { color: var(--color-danger); }

/* Loading State */
.dashboard-loading {
    opacity: 0.6;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

/* Toasts */
.toast-container {
    position: fixed;
    bottom: 24px;
    right: 24px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 1000;
}
.toast {
    background-color: var(--color-primary);
    color: #fff;
    padding: 12px 20px;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    font-weight: 500;
    box-shadow: var(--shadow-md);
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast.show {
    opacity: 1;
    transform: translateY(0);
}

.w-full { width: 100%; display: block; text-align: center; }
"""

with open(styles_path, "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("Styles appended successfully.")
