import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Alerts Center Styles
   ========================================================================== */

.alerts-layout {
    display: flex;
    gap: 24px;
    align-items: flex-start;
    position: relative;
    overflow: hidden;
}

.alerts-list-container {
    flex: 1;
    min-width: 0;
    transition: width 0.3s ease;
}

.alert-detail-panel {
    width: 400px;
    flex-shrink: 0;
    display: none;
    flex-direction: column;
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    height: calc(100vh - 280px);
    position: sticky;
    top: 24px;
}

.alert-detail-panel.active {
    display: flex;
    animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@media (max-width: 1024px) {
    .alerts-layout {
        flex-direction: column;
    }
    .alert-detail-panel {
        width: 100%;
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        height: 100vh;
        z-index: 100;
        border-radius: 0;
    }
    .alerts-list-container {
        padding: 0;
        background: transparent;
        border: none;
    }
}

/* Clickable Row */
#alertsTable tbody tr {
    cursor: pointer;
    transition: background-color 0.2s;
}
#alertsTable tbody tr:hover {
    background-color: var(--color-bg-surface-hover);
}

.alert-mobile-card {
    background: var(--color-bg-base);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

/* Severity Styling */
.severity-critical {
    color: var(--color-danger);
    font-weight: 600;
}
.severity-warning {
    color: var(--color-warning);
    font-weight: 600;
}
.severity-info {
    color: var(--color-primary);
    font-weight: 600;
}
"""

with open(styles_path, 'a', encoding='utf-8') as f:
    f.write(css_to_append)

print("Appended alerts styles successfully.")
