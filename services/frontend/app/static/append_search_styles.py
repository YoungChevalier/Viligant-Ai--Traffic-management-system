import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Search Records Styles
   ========================================================================== */

/* Search Toolbar Card */
.search-toolbar-card {
    margin-bottom: 24px;
    padding: 20px;
}
.search-primary-row {
    display: flex;
    gap: 16px;
    margin-bottom: 20px;
}
.search-input-group {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
}
.search-input-group .input-icon {
    position: absolute;
    left: 12px;
    color: var(--color-text-muted);
}
.search-input-large {
    width: 100%;
    padding-left: 40px;
    padding-right: 16px;
    height: 44px;
    font-size: 1rem;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    background-color: var(--color-bg-base);
}
.search-primary-actions {
    display: flex;
    gap: 12px;
    align-items: center;
}

/* Advanced Filters Grid */
.search-filters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--color-border);
}
.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.form-label {
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--color-text-muted);
}
.form-select {
    width: 100%;
    height: 36px;
    padding: 0 12px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    background-color: var(--color-bg-base);
    color: var(--color-text-main);
}

/* Filters Footer & Chips */
.search-filters-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px dashed var(--color-border);
}
.active-filters-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    flex: 1;
}
.filter-chip-active {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 16px;
    background-color: var(--color-primary-light);
    color: var(--color-primary);
    display: inline-flex;
    align-items: center;
    border: 1px solid rgba(0,0,0,0.05);
}
.filter-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}

/* Summary Row */
.results-summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}
.results-count {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--color-text-muted);
}
.results-actions {
    display: flex;
    gap: 16px;
    align-items: center;
}
.sort-control {
    display: flex;
    align-items: center;
    gap: 8px;
}
.sort-label {
    font-size: 0.8125rem;
    color: var(--color-text-muted);
}

/* Responsive Search */
@media (max-width: 1024px) {
    .search-primary-row { flex-direction: column; }
    .search-input-group { width: 100%; }
    .search-primary-actions { width: 100%; justify-content: flex-end; }
    .search-filters-footer { flex-direction: column; align-items: flex-start; gap: 12px; }
    .filter-actions { width: 100%; justify-content: flex-start; }
}

@media (max-width: 768px) {
    .search-filters-grid { grid-template-columns: 1fr; }
    .results-summary-row { flex-direction: column; align-items: flex-start; gap: 12px; }
    .results-actions { width: 100%; justify-content: space-between; }
    
    #searchTable thead { display: none; }
    #searchTable tbody { display: block; width: 100%; }
    
    .queue-card-mobile {
        display: block;
        padding: 16px;
        margin-bottom: 12px;
        background: var(--color-bg-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }
    .queue-card-mobile td {
        display: block;
        padding: 0;
        border: none;
    }
    .queue-card-mobile .card-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .queue-card-mobile .card-id { font-weight: 600; font-size: 0.875rem; }
    .queue-card-mobile .card-title { font-weight: 700; font-size: 1.125rem; margin-bottom: 4px; }
    .queue-card-mobile .card-meta { color: var(--color-text-muted); font-size: 0.8125rem; margin-bottom: 12px; }
    .queue-card-mobile .card-footer {
        display: flex;
        justify-content: space-between;
        padding-top: 12px;
        border-top: 1px dashed var(--color-border);
        font-size: 0.8125rem;
    }
}
"""

with open(styles_path, "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("Search Records styles appended successfully.")
