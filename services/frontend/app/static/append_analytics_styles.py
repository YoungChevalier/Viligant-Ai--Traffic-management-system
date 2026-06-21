import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Analytics Dashboard Styles
   ========================================================================== */

.analytics-kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.kpi-label {
    font-size: 13px;
    font-weight: 500;
    color: var(--color-text-muted);
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 24px;
    font-weight: 700;
    color: var(--color-text-main);
    margin-bottom: 8px;
    font-family: 'Outfit', sans-serif;
}

.kpi-trend {
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    font-weight: 500;
}

.chart-card {
    padding: 20px;
    display: flex;
    flex-direction: column;
}

.chart-toggles {
    display: flex;
    background: var(--color-bg-base);
    border-radius: 6px;
    padding: 2px;
}

.chart-toggles .btn-text {
    color: var(--color-text-muted);
}

.chart-toggles .btn-text.active {
    background: var(--color-bg-surface-hover);
    color: var(--color-text-main);
    border-radius: 4px;
}

.anpr-row {
    padding: 8px 0;
}

/* Responsive Overrides for Analytics */
@media (max-width: 1024px) {
    .analytics-charts-grid .chart-row {
        grid-template-columns: 1fr !important;
    }
}
"""

with open(styles_path, 'a', encoding='utf-8') as f:
    f.write(css_to_append)

print("Appended analytics styles successfully.")
