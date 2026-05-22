import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Voyager AI — Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session State ────────────────────────────────────────────────────────────
if "query" not in st.session_state:
    st.session_state.query = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "running" not in st.session_state:
    st.session_state.running = False

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #f7f8fa !important;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem !important;
    max-width: 900px !important;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.5rem;
}

.hero-sub {
    color: #6b7280;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.section-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #6b7280;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

textarea {
    border-radius: 12px !important;
}

.stButton > button {
    border-radius: 10px !important;
    border: none !important;
    background: #2563eb !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.7rem 1rem !important;
}

.stButton > button:hover {
    background: #1d4ed8 !important;
}

.final-wrap {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #e5e7eb;
}

.metric-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
}

.metric-label {
    color: #6b7280;
    font-size: 0.8rem;
}

[data-testid="stSidebar"] {
    background: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("## ✈️ Voyager AI")
    st.caption("Multi-agent travel planner")

    thread_id = st.text_input(
        "User ID",
        value="Prit"
    )

    st.markdown("---")

    st.markdown("### ⚙️ Agent Pipeline")

    st.markdown("1. ✈️ Flight Agent")
    st.markdown("2. 🏨 Hotel Agent")
    st.markdown("3. 🗓️ Itinerary Agent")
    st.markdown("4. 🧠 Final Agent")

    st.markdown("---")

    st.markdown("### 🧠 Powered By")

    st.markdown("- LangGraph")
    st.markdown("- Groq LLaMA")
    st.markdown("- Tavily")
    st.markdown("- PostgreSQL")

    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 🕐 Recent Queries")

        for item in reversed(st.session_state.history[-5:]):
            st.caption(item[:60])

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">
Plan Your Dream Trip with AI
</div>

<div class="hero-sub">
Flights, hotels, itinerary and complete travel planning powered by multi-agent AI.
</div>
""", unsafe_allow_html=True)

# ── Quick Buttons ────────────────────────────────────────────────────────────
QUICK = {
    "🇯🇵 Japan": "Plan a 7-day Japan trip from Mumbai under ₹2 lakhs",
    "🗼 Paris": "Plan a 5-day Paris trip from Delhi",
    "🏝️ Bali": "Plan a 10-day Bali backpacking trip",
    "🌆 Dubai": "Plan a Dubai weekend getaway from Mumbai",
}

cols = st.columns(len(QUICK))

for col, (label, value) in zip(cols, QUICK.items()):
    with col:
        if st.button(label):
            st.session_state.query = value

st.markdown("---")

# ── Input ────────────────────────────────────────────────────────────────────
# ── Input ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-label">Describe Your Trip</div>',
    unsafe_allow_html=True
)

user_query = st.text_area(
    "Travel Query",
    value=st.session_state.query,
    placeholder="Plan a 7-day Japan trip including flights, hotels and sightseeing...",
    height=120,
    label_visibility="collapsed",
)

st.session_state.query = user_query

generate = st.button(
    "🚀 Generate Travel Plan",
    use_container_width=True
)

# ── Agent Metadata ───────────────────────────────────────────────────────────
AGENT_META = {
    "flight_agent": (
        "✈️",
        "Flight Agent",
        "Searching flights"
    ),

    "hotel_agent": (
        "🏨",
        "Hotel Agent",
        "Finding hotels"
    ),

    "itinerary_agent": (
        "🗓️",
        "Itinerary Agent",
        "Building itinerary"
    ),

    "final_agent": (
        "🧠",
        "Final Agent",
        "Preparing final report"
    ),
}

# ── Generate ────────────────────────────────────────────────────────────────
if generate:

    final_query = user_query.strip()

    if not final_query:
        st.warning("Please enter your travel query.")
        st.stop()

    st.session_state.running = True

    if final_query not in st.session_state.history:
        st.session_state.history.append(final_query)

    collected = {
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "final_response": "",
        "llm_calls": 0,
    }

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    st.markdown("---")

    st.markdown("## 🤖 Agent Pipeline")

    try:

        from main import app

        for chunk in app.stream(

            {
                "messages": [
                    HumanMessage(content=final_query)
                ],

                "user_query": final_query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },

            config=config,
            stream_mode="updates",
        ):

            for node_name, state_update in chunk.items():

                icon, title, subtitle = AGENT_META.get(
                    node_name,
                    ("🔧", node_name, "Processing")
                )

                with st.status(
                    f"{icon} {title}",
                    expanded=True,
                    state="complete"
                ):

                    st.caption(subtitle)

                    # ── Flight Agent ──
                    if node_name == "flight_agent":

                        text = state_update.get(
                            "flight_results",
                            ""
                        )

                        collected["flight_results"] = text

                        if text:
                            st.markdown(text)
                        else:
                            st.info("No flight data returned.")

                    # ── Hotel Agent ──
                    elif node_name == "hotel_agent":

                        text = state_update.get(
                            "hotel_results",
                            ""
                        )

                        collected["hotel_results"] = text

                        if text:
                            st.markdown(text)
                        else:
                            st.info("No hotel data returned.")

                    # ── Itinerary Agent ──
                    elif node_name == "itinerary_agent":

                        text = state_update.get(
                            "itinerary",
                            ""
                        )

                        collected["itinerary"] = text

                        if text:
                            st.markdown(text)
                        else:
                            st.info("No itinerary generated.")

                    # ── Final Agent ──
                    elif node_name == "final_agent":

                        msgs = state_update.get(
                            "messages",
                            []
                        )

                        text = ""

                        if msgs:
                            try:
                                text = msgs[-1].content
                            except:
                                text = str(msgs[-1])

                        collected["final_response"] = text

                        if text:
                            st.markdown(text)
                        else:
                            st.info("No final response.")

                    # ── LLM Calls ──
                    llm_calls = state_update.get("llm_calls")

                    if llm_calls is not None:
                        collected["llm_calls"] = llm_calls

    except Exception as e:

        st.error(f"Error: {e}")

        st.stop()

    finally:

        st.session_state.running = False

    # ── Metrics ─────────────────────────────────────────────────────────────
    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">4</div>
            <div class="metric-label">Agents</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{collected['llm_calls']}</div>
            <div class="metric-label">LLM Calls</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-value">✅</div>
            <div class="metric-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Final Response ─────────────────────────────────────────────────────
    if collected["final_response"]:

        st.markdown("---")

        st.markdown("## 🧠 Final Travel Plan")

        st.markdown(
            '<div class="final-wrap">',
            unsafe_allow_html=True
        )

        st.markdown(collected["final_response"])

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ── Save File ──────────────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"travel_plan_{timestamp}.md"

    file_content = f"""
# Travel Plan

## Query
{final_query}

## Flight Information
{collected['flight_results']}

## Hotel Information
{collected['hotel_results']}

## Itinerary
{collected['itinerary']}

## Final Plan
{collected['final_response']}
"""

    save_dir = os.path.join(
        os.path.dirname(__file__),
        "travel_plans"
    )

    os.makedirs(save_dir, exist_ok=True)

    with open(
        os.path.join(save_dir, filename),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(file_content)

    st.download_button(
        "⬇️ Download Plan",
        data=file_content,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )

    st.success(f"Saved to travel_plans/{filename}")

