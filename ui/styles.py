import streamlit as st


def apply_styles(dark_theme=True):
    if dark_theme:
        colors = {
            "bg": "#070b14",
            "panel": "#0f172a",
            "panel_soft": "#111c33",
            "text": "#f8fafc",
            "muted": "#a7b0c0",
            "border": "#24324a",
            "primary": "#38bdf8",
            "primary_dark": "#0284c7",
            "soft": "#172554",
            "grid": "rgba(148, 163, 184, 0.12)",
            "hero_a": "rgba(56, 189, 248, 0.14)",
            "hero_b": "rgba(45, 212, 191, 0.1)",
            "shadow": "rgba(0, 0, 0, 0.28)",
            "input": "#0b1220",
        }
    else:
        colors = {
            "bg": "#f6f7fb",
            "panel": "#ffffff",
            "panel_soft": "#f8fafc",
            "text": "#111827",
            "muted": "#6b7280",
            "border": "#e5e7eb",
            "primary": "#2563eb",
            "primary_dark": "#1d4ed8",
            "soft": "#eef2ff",
            "grid": "rgba(37, 99, 235, 0.08)",
            "hero_a": "rgba(37, 99, 235, 0.08)",
            "hero_b": "rgba(20, 184, 166, 0.08)",
            "shadow": "rgba(15, 23, 42, 0.08)",
            "input": "#ffffff",
        }

    css_vars = "\n".join(
        [
            f"    --viaai-bg: {colors['bg']};",
            f"    --viaai-panel: {colors['panel']};",
            f"    --viaai-panel-soft: {colors['panel_soft']};",
            f"    --viaai-text: {colors['text']};",
            f"    --viaai-muted: {colors['muted']};",
            f"    --viaai-border: {colors['border']};",
            f"    --viaai-primary: {colors['primary']};",
            f"    --viaai-primary-dark: {colors['primary_dark']};",
            f"    --viaai-soft: {colors['soft']};",
            f"    --viaai-grid: {colors['grid']};",
            f"    --viaai-hero-a: {colors['hero_a']};",
            f"    --viaai-hero-b: {colors['hero_b']};",
            f"    --viaai-shadow: {colors['shadow']};",
            f"    --viaai-input: {colors['input']};",
        ]
    )

    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
__CSS_VARS__
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--viaai-bg) !important;
    font-family: 'Inter', sans-serif;
    color: var(--viaai-text) !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.stApp,
.main,
[data-testid="stMarkdownContainer"],
[data-testid="stText"],
p,
li,
h1,
h2,
h3,
h4,
h5,
h6,
label {
    color: var(--viaai-text) !important;
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
        linear-gradient(135deg, var(--viaai-hero-a), var(--viaai-hero-b)),
        var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    margin: 2rem 0 1.25rem;
    min-height: 340px;
    overflow: hidden;
    padding: 3rem;
    position: relative;
}

.start-shell::after {
    animation: sweep 5s ease-in-out infinite;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.16), transparent);
    content: "";
    height: 100%;
    left: -55%;
    position: absolute;
    top: 0;
    transform: skewX(-18deg);
    width: 40%;
    z-index: 1;
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
    background: var(--viaai-panel-soft);
    border: 1px solid var(--viaai-border);
    border-radius: 999px;
    color: var(--viaai-text);
    font-size: 0.85rem;
    font-weight: 650;
    padding: 0.5rem 0.75rem;
    transition: transform 180ms ease, border-color 180ms ease;
}

.feature-row span:hover {
    border-color: var(--viaai-primary);
    transform: translateY(-3px);
}

.start-grid {
    animation: drift 18s linear infinite;
    background-image:
        linear-gradient(var(--viaai-grid) 1px, transparent 1px),
        linear-gradient(90deg, var(--viaai-grid) 1px, transparent 1px);
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

.chat-shell {
    animation: fadeUp 650ms ease-out both;
    background:
        linear-gradient(135deg, var(--viaai-hero-a), transparent 55%),
        var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    box-shadow: 0 18px 45px var(--viaai-shadow);
    margin-bottom: 0.75rem;
    overflow: hidden;
    padding: 1rem 1.1rem;
    position: relative;
}

.chat-shell::before {
    animation: pulseRing 2.8s ease-in-out infinite;
    background: var(--viaai-primary);
    border-radius: 999px;
    content: "";
    height: 9px;
    position: absolute;
    right: 1rem;
    top: 1rem;
    width: 9px;
}

.chat-header {
    align-items: center;
    display: flex;
    gap: 1rem;
    justify-content: space-between;
}

.chat-title {
    color: var(--viaai-text);
    font-size: 1.05rem;
    font-weight: 750;
}

.chat-pulse {
    background: var(--viaai-panel-soft);
    border: 1px solid var(--viaai-border);
    border-radius: 999px;
    color: var(--viaai-muted);
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.45rem 0.75rem;
}

.final-wrap {
    background: var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    padding: 1.35rem;
    animation: fadeUp 650ms ease-out both;
}

.metric-box {
    background: var(--viaai-panel);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    transition: transform 180ms ease, border-color 180ms ease;
}

.metric-box:hover {
    border-color: var(--viaai-primary);
    transform: translateY(-4px);
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

textarea,
input,
[data-baseweb="textarea"] textarea,
[data-baseweb="input"] input {
    background: var(--viaai-input) !important;
    border-color: var(--viaai-border) !important;
    color: var(--viaai-text) !important;
}

textarea::placeholder,
input::placeholder {
    color: var(--viaai-muted) !important;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stLinkButton"] a {
    border-radius: 8px !important;
    font-weight: 650 !important;
}

.theme-toggle-label {
    color: var(--viaai-muted);
    font-size: 0.74rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    margin-bottom: 0.25rem;
    text-align: center;
    text-transform: uppercase;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) {
    align-items: center;
    display: flex;
    justify-content: center;
    background: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 999px !important;
    box-shadow: 0 14px 34px var(--viaai-shadow);
    height: 34px !important;
    min-width: 74px !important;
    padding: 3px !important;
    position: relative;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]):hover {
    transform: translateY(-1px);
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) [data-testid="stMarkdownContainer"],
label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) p {
    display: none !important;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) span {
    border-radius: 999px !important;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) > div:first-child {
    background: transparent !important;
    border: none !important;
    height: 28px !important;
    position: relative !important;
    width: 68px !important;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) > div:first-child::before {
    color: #0f172a;
    content: "Light";
    font-size: 0.68rem;
    font-weight: 800;
    left: 8px;
    line-height: 28px;
    position: absolute;
    top: 0;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) > div:first-child::after {
    color: #0f172a;
    content: "Dark";
    font-size: 0.68rem;
    font-weight: 800;
    line-height: 28px;
    position: absolute;
    right: 8px;
    top: 0;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) input {
    cursor: pointer !important;
    inset: 0 !important;
    opacity: 0 !important;
    position: absolute !important;
    z-index: 4 !important;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"]) > div:first-child > div {
    display: none !important;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"])::before {
    background: transparent !important;
    border: none !important;
    height: 28px !important;
    left: 3px !important;
    position: absolute !important;
    top: 3px !important;
    width: 68px !important;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"])::after {
    background: var(--viaai-primary);
    border-radius: 999px;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.22);
    content: "";
    height: 28px;
    left: 0;
    position: absolute;
    top: 0;
    transition: transform 260ms ease;
    width: 34px;
    z-index: 2;
}

label[data-baseweb="checkbox"]:has(input[aria-label="Theme"][aria-checked="true"])::after {
    transform: translateX(34px);
}

.stButton > button {
    background: #ffffff !important;
    border: 1px solid #ffffff !important;
    color: #0f172a !important;
}

.stButton > button *,
.stButton > button p {
    color: #0f172a !important;
}

.stButton > button:hover {
    background: #f8fafc !important;
    border-color: #f8fafc !important;
    color: #0f172a !important;
}

.stButton > button[kind="primary"],
.stDownloadButton > button,
[data-testid="stLinkButton"] a {
    background: var(--viaai-primary) !important;
    border-color: var(--viaai-primary) !important;
    color: white !important;
}

.stButton > button[kind="primary"] *,
.stButton > button[kind="primary"] p,
.stDownloadButton > button *,
.stDownloadButton > button p,
[data-testid="stLinkButton"] a *,
[data-testid="stLinkButton"] a p {
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
    background: var(--viaai-panel-soft);
    border: 1px solid var(--viaai-border);
    border-radius: 8px;
    box-shadow: 0 18px 45px var(--viaai-shadow);
    display: grid;
    gap: 0.2rem;
    min-width: 155px;
    padding: 0.95rem 1rem;
    position: absolute;
    right: 8%;
    z-index: 2;
    transition: transform 180ms ease, border-color 180ms ease;
}

.route-card:hover {
    border-color: var(--viaai-primary);
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

@keyframes sweep {
    0%, 35% {
        left: -55%;
    }
    70%, 100% {
        left: 125%;
    }
}

@keyframes pulseRing {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.32);
    }
    50% {
        box-shadow: 0 0 0 10px rgba(56, 189, 248, 0);
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

    .chat-header {
        align-items: flex-start;
        flex-direction: column;
    }
}
</style>
""".replace("__CSS_VARS__", css_vars),
        unsafe_allow_html=True,
    )
