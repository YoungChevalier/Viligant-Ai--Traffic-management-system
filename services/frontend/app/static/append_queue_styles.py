import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Review Queue Additional Styles
   ========================================================================== */

/* Filter Toolbar */
.filter-toolbar {
    margin-bottom: 20px;
}
.filter-row {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    padding: 16px;
    align-items: center;
}
.filter-group {
    display: flex;
    flex-direction: column;
}
.flex-1 { flex: 1; min-width: 200px; }

.form-select {
    height: 36px;
    padding: 6px 32px 6px 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background-color: var(--color-bg-base);
    color: var(--color-text-main);
    font-family: inherit;
    font-size: 0.875rem;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 10px center;
    cursor: pointer;
}
.form-select:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px var(--color-primary-light);
}
.form-checkbox {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid var(--color-border);
    cursor: pointer;
    accent-color: var(--color-primary);
}

/* Tabs Navigation */
.tabs-row {
    display: flex;
    border-bottom: 1px solid var(--color-border);
    margin-bottom: 24px;
    gap: 24px;
    overflow-x: auto;
    scrollbar-width: none;
}
.tabs-row::-webkit-scrollbar { display: none; }
.tab-item {
    padding: 12px 4px;
    font-weight: 500;
    font-size: 0.875rem;
    color: var(--color-text-muted);
    border-bottom: 2px solid transparent;
    transition: all 0.2s ease;
    white-space: nowrap;
}
.tab-item:hover { color: var(--color-text-main); }
.tab-item.active {
    color: var(--color-primary);
    border-bottom-color: var(--color-primary);
    font-weight: 600;
}
.tab-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background-color: var(--color-bg-base);
    color: var(--color-text-muted);
    border-radius: var(--radius-full);
    font-size: 0.6875rem;
    padding: 2px 8px;
    margin-left: 6px;
}
.tab-item.active .tab-count {
    background-color: var(--color-primary-light);
    color: var(--color-primary);
}

/* Queue Specific Columns */
.col-check { width: 40px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.col-thumb { width: 60px; flex-shrink: 0; }
.col-assign { width: 14%; flex-shrink: 0; }
.col-actions { width: 100px; flex-shrink: 0; }
.col-id { width: 12%; flex-shrink: 0; }
.col-type { width: 18%; flex-shrink: 0; }
.col-plate { width: 12%; flex-shrink: 0; }
.col-cam { width: 14%; flex-shrink: 0; }
.col-time { width: 10%; flex-shrink: 0; }
.col-score { width: 8%; flex-shrink: 0; }
.col-status { width: 100px; flex-shrink: 0; }

.thumb-placeholder {
    width: 36px;
    height: 36px;
    background-color: var(--color-bg-base);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}
.queue-row {
    display: flex;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--color-border);
    font-size: 0.875rem;
    transition: background-color 0.2s ease;
}
.queue-row:last-child { border-bottom: none; }
.queue-row:hover:not(.header) {
    background-color: var(--color-bg-surface-hover);
    cursor: pointer;
}
.queue-row.header {
    background-color: var(--color-bg-base);
    font-weight: 600;
    color: var(--color-text-muted);
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding-top: 10px;
    padding-bottom: 10px;
    position: sticky;
    top: 0;
    z-index: 10;
}

.text-right { text-align: right; justify-content: flex-end; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.text-muted { color: var(--color-text-muted); }
.text-success { color: var(--color-success); }
.text-warning { color: var(--color-warning); }

.action-menu-compact {
    display: flex;
    gap: 4px;
    justify-content: flex-end;
}
.btn-sm { padding: 4px 8px; font-size: 0.75rem; height: 28px; border-radius: var(--radius-sm); }
.action-approve { color: var(--color-success); background-color: rgba(34,197,94,0.1); }
.action-approve:hover { background-color: var(--color-success); color: white; }
.action-reject { color: var(--color-danger); background-color: rgba(239,68,68,0.1); }
.action-reject:hover { background-color: var(--color-danger); color: white; }

/* Bulk Action Bar */
.bulk-action-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 56px;
    background-color: var(--color-primary-light);
    border-bottom: 1px solid var(--color-border);
    border-top-left-radius: var(--radius-lg);
    border-top-right-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    z-index: 20;
    opacity: 0;
    pointer-events: none;
    transform: translateY(-10px);
    transition: all 0.2s ease;
}
.bulk-action-bar.visible {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0);
}
.bulk-count {
    font-weight: 600;
    color: var(--color-primary);
}
.bulk-actions { display: flex; gap: 8px; }

/* State Containers */
.state-container {
    padding: 60px 20px;
    text-align: center;
    color: var(--color-text-muted);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.state-icon { font-size: 3rem; margin-bottom: 16px; }
.state-container h3 { color: var(--color-text-main); margin-bottom: 8px; }
.loader-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--color-border);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Desktop vs Mobile Toggle */
.queue-mobile-container { display: none; }

/* Mobile Responsive */
@media (max-width: 1024px) {
    .filter-group { flex: 1; min-width: calc(50% - 12px); }
    .col-cam, .col-assign { display: none; }
}

@media (max-width: 768px) {
    .queue-table-container { display: none; }
    .queue-mobile-container { display: flex; flex-direction: column; padding: 12px; gap: 12px; }
    
    .queue-card-mobile {
        background-color: var(--color-bg-base);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: 12px;
    }
    .card-mobile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--color-border);
    }
    .card-mobile-body {
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    .card-mobile-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .card-mobile-actions {
        display: flex;
        gap: 8px;
        margin-top: 16px;
    }
}
"""

with open(styles_path, "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("Queue styles appended successfully.")
