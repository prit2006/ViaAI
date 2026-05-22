import streamlit as st


def apply_styles():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --viaai-bg: #f6f7fb;
    --viaai-panel: #ffffff;
    --viaai-text: #111827;
    --viaai-muted: #6b7280;
    --viaai-border: #e5e7eb;
    --viaai-primary: #2563eb;
    --viaai-primary-dark: #1d4ed8;
    --viaai-soft: #eef2ff;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--viaai-bg) !important;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 980px !important;
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

[data-testid="stSidebar"] {
    background: var(--viaai-panel) !important;
    border-right: 1px solid var(--viaai-border);
}

.viaai-kicker {
    color: var(--viaai-primary);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
    text-transform: uppercase;
}

.viaai-title {
    color: var(--viaai-text);
    font-size: 2.3rem;
    font-weight: 750;
    line-height: 1.1;
    margin-bottom: 0.55rem;
}

.viaai-subtitle {
    color: var(--viaai-muted);
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.section-label {
    color: var(--viaai-muted);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
}

.final-wrap {
    background: var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    padding: 1.35rem;
}

.metric-box {
    background: var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    color: var(--viaai-text);
    font-size: 1.35rem;
    font-weight: 750;
}

.metric-label {
    color: var(--viaai-muted);
    font-size: 0.82rem;
    margin-top: 0.15rem;
}

textarea {
    border-radius: 8px !important;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stLinkButton"] a {
    border-radius: 8px !important;
    font-weight: 650 !important;
}

.stButton > button[kind="primary"],
.stDownloadButton > button,
[data-testid="stLinkButton"] a {
    background: var(--viaai-primary) !important;
    border-color: var(--viaai-primary) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover,
.stDownloadButton > button:hover,
[data-testid="stLinkButton"] a:hover {
    background: var(--viaai-primary-dark) !important;
    border-color: var(--viaai-primary-dark) !important;
    color: white !important;
}

hr {
    border-color: var(--viaai-border);
}
</style>
""",
        unsafe_allow_html=True,
    )
