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
    font-size: 14px;
    font-weight: 500;
    color: #8a837c;
    letter-spacing: 0.03em;
    font-style: italic;
    opacity: 0.9;
}

.answer {
    font-size: 20px;
    font-weight: 600;
    color: #2d2a26;
}

.media-wrap {
    padding: 16px;
    background: #ffffff;
    border: 1.5px solid #e8e4df;
    border-radius: 12px;
    max-width: 280px;
    width: 100%;
    margin: 0 auto;
    box-shadow: 0 4px 12px rgba(45, 42, 38, 0.04);
}
.media-wrap img {
    display: block;
    margin: 0 auto;
    max-width: 100%;
    height: auto;
}

.quark-text {
    font-size: 20px;
    font-weight: 500;
    color: #4a4642;
    letter-spacing: 0.1em;
    font-family: "Georgia", "Times New Roman", serif;
}

.mass-value {
    font-size: 32px;
    font-weight: 700;
    color: #1f1d1a;
    background: #ffffff;
    padding: 12px 24px;
    border: 2px solid #e8e4df;
    border-radius: 12px;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
}

.meta {
    font-size: 13px;
    color: #9a9590;
    font-family: "SF Mono", "Consolas", monospace;
    opacity: 0.8;
}

/* ── Anki Default Override ── */

hr#answer {
    border: none;
    border-top: 1px dashed #dcd8d3;
    margin: 24px 0;
    width: 60%;
}
"""
