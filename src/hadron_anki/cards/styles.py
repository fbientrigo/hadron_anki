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
    padding: 32px 24px;
    font-family: "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
    color: #2d2a26;
    background: #faf8f5;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(45, 42, 38, 0.08);
    line-height: 1.5;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.title {
    font-size: 26px;
    font-weight: 700;
    color: #2d2a26;
    letter-spacing: -0.01em;
}

.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 3px 12px;
    border-radius: 100px;
    color: #ffffff;
}
.badge.baryon { background: #4a7c59; }
.badge.meson { background: #7c5a4a; }

.prompt {
    font-size: 15px;
    font-weight: 500;
    color: #6b6560;
    letter-spacing: 0.02em;
    font-style: italic;
}

.answer {
    font-size: 20px;
    font-weight: 600;
    color: #2d2a26;
}

.media-wrap {
    padding: 12px;
    background: #ffffff;
    border: 1.5px solid #e8e4df;
    border-radius: 10px;
}
.media-wrap img {
    display: block;
    max-width: 100%;
    height: auto;
}

.quark-text {
    font-size: 22px;
    letter-spacing: 0.12em;
    font-family: "Georgia", "Times New Roman", serif;
}

.mass-value {
    color: #2d2a26;
    background: #ffffff;
    padding: 8px 16px;
    border: 1.5px solid #e8e4df;
    border-radius: 8px;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
}

.meta {
    font-size: 13px;
    color: #9a9590;
    font-family: "SF Mono", "Consolas", monospace;
    margin-top: 8px;
}

/* ── Anki Default Override ── */

hr#answer {
    border: none;
    border-top: 1px dashed #e8e4df;
    margin: 20px 0;
    width: 60%;
}
"""
