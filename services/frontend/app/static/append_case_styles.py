import os

styles_path = r"c:\Users\Lenovo\Desktop\Languages\Traffic Management System\services\frontend\app\static\styles.css"

css_to_append = """

/* ==========================================================================
   Case Detail Additional Styles
   ========================================================================== */

/* Layout Grid */
.case-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
    align-items: start;
}
.case-details-split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

/* Evidence Viewer */
.evidence-viewer-wrapper {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background-color: #000;
    overflow: hidden;
    border-bottom: 1px solid var(--color-border);
}
.evidence-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: var(--color-text-muted);
    position: relative;
    transition: background-color 0.3s ease;
}
.evidence-icon {
    font-size: 3rem;
    margin-bottom: 12px;
}
.bbox {
    position: absolute;
    border: 2px solid transparent;
    background-color: rgba(0,0,0,0.5);
    color: white;
    font-size: 0.75rem;
    padding: 2px 6px;
    font-weight: 600;
}
.bbox-plate {
    border-color: var(--color-danger);
    background-color: rgba(239,68,68,0.2);
    top: 60%;
    left: 45%;
    width: 120px;
    height: 40px;
    display: flex;
    align-items: flex-end;
}
.bbox-vehicle {
    border-color: var(--color-success);
    background-color: rgba(34,197,94,0.1);
    top: 30%;
    left: 30%;
    width: 40%;
    height: 60%;
}

.thumbnail-strip {
    display: flex;
    gap: 8px;
}
.thumb-item {
    width: 48px;
    height: 36px;
    background-color: var(--color-bg-surface-hover);
    border: 2px solid transparent;
    border-radius: var(--radius-sm);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--color-text-muted);
    transition: all 0.2s ease;
}
.thumb-item:hover { border-color: var(--color-border); }
.thumb-item.active {
    border-color: var(--color-primary);
    color: var(--color-primary);
}

/* Toggle Switch */
.toggle-switch {
    position: relative;
    display: inline-flex;
    align-items: center;
    cursor: pointer;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.toggle-slider {
    position: relative;
    width: 36px;
    height: 20px;
    background-color: var(--color-border);
    border-radius: 20px;
    transition: .4s;
}
.toggle-slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    border-radius: 50%;
    transition: .4s;
}
.toggle-switch input:checked + .toggle-slider { background-color: var(--color-primary); }
.toggle-switch input:checked + .toggle-slider:before { transform: translateX(16px); }

/* Summary & OCR Panels */
.summary-stat-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px dashed var(--color-border);
    font-size: 0.875rem;
}
.summary-stat-row:last-child { border-bottom: none; }
.stat-label { color: var(--color-text-muted); }
.ai-reasoning-box {
    margin-top: 16px;
    background-color: var(--color-bg-surface-hover);
    padding: 12px;
    border-radius: var(--radius-sm);
    border-left: 3px solid var(--color-primary);
}
.reasoning-title { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--color-text-muted); margin-bottom: 4px; }
.reasoning-text { font-size: 0.875rem; line-height: 1.5; color: var(--color-text-main); }

.ocr-plate-display {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-align: center;
    padding: 12px;
    background-color: var(--color-bg-surface-hover);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-md);
    font-family: monospace;
}
.ocr-crop-placeholder {
    width: 100%;
    height: 60px;
    background-color: #e2e8f0;
    border: 1px dashed var(--color-border);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-sm);
}
.ocr-crop-placeholder .crop-text { color: var(--color-text-muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; }

/* Metadata List */
.meta-list { display: flex; flex-direction: column; gap: 8px; }
.meta-item { display: flex; justify-content: space-between; font-size: 0.875rem; }
.meta-label { color: var(--color-text-muted); }
.meta-divider { height: 1px; background-color: var(--color-border); margin: 4px 0; }
.color-swatch { display: inline-block; width: 12px; height: 12px; border-radius: 50%; border: 1px solid var(--color-border); vertical-align: middle; }

/* Timeline */
.timeline {
    position: relative;
    padding-left: 20px;
}
.timeline::before {
    content: '';
    position: absolute;
    left: 7px;
    top: 8px;
    bottom: 0;
    width: 2px;
    background-color: var(--color-border);
}
.timeline-item {
    position: relative;
    margin-bottom: 24px;
}
.timeline-item:last-child { margin-bottom: 0; }
.timeline-dot {
    position: absolute;
    left: -20px;
    top: 4px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: var(--color-text-muted);
    border: 3px solid var(--color-bg-base);
}
.bg-success { background-color: var(--color-success); }
.bg-primary { background-color: var(--color-primary); }
.bg-warning { background-color: var(--color-warning); }
.bg-danger { background-color: var(--color-danger); }

.timeline-content { padding-left: 12px; }
.timeline-title { font-weight: 600; font-size: 0.875rem; margin-bottom: 2px; }
.timeline-desc { font-size: 0.8125rem; color: var(--color-text-main); margin-bottom: 4px; }
.timeline-time { font-size: 0.75rem; color: var(--color-text-muted); }

/* Responsive adjustments */
@media (max-width: 1024px) {
    .case-grid { grid-template-columns: 1fr; }
    .case-details-split { grid-template-columns: 1fr; }
}
"""

with open(styles_path, "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("Case detail styles appended successfully.")
