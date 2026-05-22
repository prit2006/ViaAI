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

.start-shell {
    animation: fadeUp 700ms ease-out both;
    background:
        linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(20, 184, 166, 0.08)),
        var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    margin: 2rem 0 1.25rem;
    min-height: 340px;
    overflow: hidden;
    padding: 3rem;
    position: relative;
}

.start-copy {
    max-width: 680px;
    position: relative;
    z-index: 2;
}

.start-title {
    animation: slideIn 800ms ease-out both;
    font-size: 4.4rem;
    letter-spacing: 0;
}

.start-subtitle {
    animation: slideIn 900ms ease-out both;
    font-size: 1.1rem;
    max-width: 620px;
}

.feature-row {
    animation: fadeUp 950ms ease-out both;
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 1.4rem;
}

.feature-row span {
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(37, 99, 235, 0.12);
    border-radius: 999px;
    color: var(--viaai-text);
    font-size: 0.85rem;
    font-weight: 650;
    padding: 0.5rem 0.75rem;
}

.start-grid {
    animation: drift 18s linear infinite;
    background-image:
        linear-gradient(rgba(37, 99, 235, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37, 99, 235, 0.08) 1px, transparent 1px);
    background-size: 42px 42px;
    inset: 0;
    opacity: 0.9;
    position: absolute;
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

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-16px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes drift {
    from {
        transform: translate3d(0, 0, 0);
    }
    to {
        transform: translate3d(42px, 42px, 0);
    }
}

.route-card {
    animation: floatCard 6s ease-in-out infinite;
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid rgba(37, 99, 235, 0.16);
    border-radius: 8px;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    display: grid;
    gap: 0.2rem;
    min-width: 155px;
    padding: 0.95rem 1rem;
    position: absolute;
    right: 8%;
    z-index: 2;
}

.route-card strong {
    color: var(--viaai-text);
    font-size: 0.98rem;
}

.route-card span {
    color: var(--viaai-muted);
    font-size: 0.82rem;
}

.route-card-one {
    top: 22%;
}

.route-card-two {
    animation-delay: 900ms;
    bottom: 19%;
    right: 18%;
}

.route-line {
    animation: routePulse 2.8s ease-in-out infinite;
    background: linear-gradient(90deg, transparent, var(--viaai-primary), transparent);
    height: 2px;
    opacity: 0.5;
    position: absolute;
    right: 11%;
    top: 55%;
    transform: rotate(-24deg);
    width: 270px;
    z-index: 1;
}

@keyframes floatCard {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-12px);
    }
}

@keyframes routePulse {
    0%, 100% {
        opacity: 0.25;
    }
    50% {
        opacity: 0.75;
    }
}

@media (max-width: 720px) {
    .start-shell {
        min-height: 310px;
        padding: 2rem;
    }

    .start-title {
        font-size: 3rem;
    }

    .route-card,
    .route-line {
        display: none;
    }
}
</style>
""",
        unsafe_allow_html=True,
    )
