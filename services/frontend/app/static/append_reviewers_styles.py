import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Reviewers Dashboard Styles
   ========================================================================== */

.reviewers-layout {
    display: flex;
    gap: 24px;
    align-items: flex-start;
    position: relative;
    overflow: hidden;
}

.reviewers-list-container {
    flex: 1;
    min-width: 0;
    transition: width 0.3s ease;
}

.reviewer-detail-panel {
    width: 380px;
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

.reviewer-detail-panel.active {
    display: flex;
    animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@media (max-width: 1024px) {
    .reviewers-layout {
        flex-direction: column;
    }
    .reviewer-detail-panel {
        width: 100%;
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        height: 100vh;
        z-index: 100;
        border-radius: 0;
    }
    .reviewers-list-container {
        padding: 0;
        background: transparent;
        border: none;
    }
}

/* Clickable Row */
#reviewersTable tbody tr {
    cursor: pointer;
    transition: background-color 0.2s;
}
#reviewersTable tbody tr:hover {
    background-color: var(--color-bg-surface-hover);
}

.reviewer-mobile-card {
    background: var(--color-bg-base);
    border: 1px solid var(--color-border);
    border-radius: 8px;
    padding: 16px;
}
"""

with open(styles_path, 'a', encoding='utf-8') as f:
    f.write(css_to_append)

print("Appended reviewers styles successfully.")
