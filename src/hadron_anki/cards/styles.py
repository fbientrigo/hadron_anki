"""
CSS design system for Anki cards.

CSS is defined once here and injected into:
- genanki.Model(css=CARD_CSS) for .apkg packaging
- preview HTML <style> tag for browser preview
"""

CARD_CSS: str = """\
/* ── Hadron Anki — Shared Template CSS ── */

.card-shell {
    max-width: 420px;
    margin: 0 auto;
    padding: 36px 28px;
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    color: #2d2a26;
    background: #faf8f5;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(45, 42, 38, 0.05);
    line-height: 1.5;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
    min-height: 200px;
}

.title {
    font-size: 28px;
    font-weight: 700;
    color: #2d2a26;
    letter-spacing: -0.01em;
}

.title-row {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: 12px;
}

.title-name {
    font-size: 28px;
    font-weight: 700;
    color: #2d2a26;
    letter-spacing: -0.01em;
}

.title-tex {
    font-size: 24px;
    color: #4a4642;
    opacity: 0.9;
}

.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 4px 14px;
    border-radius: 100px;
    color: #ffffff;
    margin-bottom: 4px;
}
.badge.baryon { background: #4a7c59; }
.badge.meson { background: #7c5a4a; }

.prompt {
    font-size: 13px;
    font-weight: 500;
    color: #9a9590;
    letter-spacing: 0.04em;
    font-style: italic;
    opacity: 0.85;
    margin-bottom: 4px;
}

.answer {
    font-size: 20px;
    font-weight: 600;
    color: #2d2a26;
}

.media-wrap {
    padding: 16px;
    background: #ffffff;
    border: 1px solid #e8e4df;
    border-radius: 12px;
    width: 100%;
    max-width: 320px;
    box-sizing: border-box;
    margin: 0 auto;
    box-shadow: 0 2px 8px rgba(45, 42, 38, 0.04);
    display: flex;
    justify-content: center;
    align-items: center;
}
.media-wrap img {
    display: block;
    max-width: 100%;
    height: auto;
    object-fit: contain;
}

.quark-text {
    font-size: 18px;
    font-weight: 500;
    color: #6b6560;
    letter-spacing: 0.12em;
    font-family: "Georgia", "Times New Roman", serif;
}

.large-quarks {
    font-size: 36px;
    color: #2d2a26;
    letter-spacing: 0.15em;
    margin: 12px 0;
}

.mass-value {
    font-size: 48px;
    font-weight: 800;
    color: #2d2a26;
    letter-spacing: -0.02em;
    font-family: "Inter", "Segoe UI", system-ui, sans-serif;
    margin: 8px 0;
}

.meta {
    font-size: 12px;
    color: #a39f9a;
    font-family: "SF Mono", "Consolas", monospace;
    opacity: 0.7;
    margin-top: 12px;
}

.badge.octet { background: #5a6b7c; }

/* ── Modular concept sections (summary card + future split cards) ── */

.section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 12px 0;
    border-top: 1px solid #ece8e3;
}

.section-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9a9590;
}

.mass-summary {
    font-size: 18px;
    font-weight: 600;
    color: #2d2a26;
}

.decay-line {
    font-size: 18px;
    font-weight: 500;
    color: #2d2a26;
    font-family: "Georgia", "Times New Roman", serif;
}

/* ── Anki Default Override ── */

hr#answer {
    border: none;
    border-top: 1px dashed #dcd8d3;
    margin: 24px 0;
    width: 60%;
}
"""
