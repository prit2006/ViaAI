import streamlit as st

from ui import auth


QUICK_PROMPTS = {
    "Japan": "Plan a 7-day Japan trip from Mumbai under 2 lakhs INR",
    "Paris": "Plan a 5-day Paris trip from Delhi",
    "Bali": "Plan a 10-day Bali backpacking trip",
    "Dubai": "Plan a Dubai weekend getaway from Mumbai",
}


def show_login_screen():
    login_url = auth.build_login_url()

    st.markdown(
        """
<div class="start-shell">
    <div class="start-grid"></div>
    <div class="route-card route-card-one">
        <strong>Mumbai</strong>
        <span>to Tokyo</span>
    </div>
    <div class="route-card route-card-two">
        <strong>Hotel</strong>
        <span>4 options found</span>
    </div>
    <div class="route-line"></div>
    <div class="start-copy">
        <div class="viaai-kicker">Private AI travel planning</div>
        <div class="viaai-title start-title">ViaAI</div>
        <div class="viaai-subtitle start-subtitle">
            Build interactive travel plans with flights, hotels, itineraries, and saved memory.
        </div>
        <div class="feature-row">
            <span>Flight search</span>
            <span>Hotel context</span>
            <span>Itinerary builder</span>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if not auth.is_auth_configured():
        st.warning(
            "Clerk OAuth is not configured yet. Fill .streamlit/secrets.toml "
            "with your Clerk OAuth client ID and client secret, then restart Streamlit."
        )
        st.code(
            """
[auth]
redirect_uri = "http://localhost:8501"
cookie_secret = "CHANGE_ME_TO_A_LONG_RANDOM_VALUE"
client_id = "CHANGE_ME_CLERK_OAUTH_CLIENT_ID"
client_secret = "CHANGE_ME_CLERK_OAUTH_CLIENT_SECRET"
server_metadata_url = "https://YOUR_CLERK_DOMAIN.clerk.accounts.dev/.well-known/openid-configuration"
client_kwargs = { "scope" = "profile email" }
""".strip(),
            language="toml",
        )
        st.stop()

    login_col, signup_col = st.columns(2)
    with login_col:
        st.link_button(
            "Log in",
            login_url,
            type="primary",
            use_container_width=True,
        )
    with signup_col:
        st.link_button(
            "Sign up",
            login_url,
            use_container_width=True,
        )
    st.stop()


def render_sidebar(thread_id, signed_in_name, signed_in_email, history):
    with st.sidebar:
        st.markdown("## ViaAI")
        st.caption("Multi-agent travel planner")

        st.markdown("### Account")
        st.write(signed_in_name or "Signed in")
        if signed_in_email:
            st.caption(signed_in_email)
        st.caption(f"Memory ID: {thread_id}")

        if st.button("Log out", use_container_width=True):
            auth.logout()

        st.markdown("---")
        st.markdown("### Agent Pipeline")
        st.markdown("1. Flight Agent")
        st.markdown("2. Hotel Agent")
        st.markdown("3. Itinerary Agent")
        st.markdown("4. Final Agent")

        st.markdown("---")
        st.markdown("### Powered By")
        st.markdown("- LangGraph")
        st.markdown("- Groq LLaMA")
        st.markdown("- Tavily")
        st.markdown("- PostgreSQL")
        st.markdown("- Clerk")

        if history:
            st.markdown("---")
            st.markdown("### Recent Queries")
            for item in reversed(history[-5:]):
                st.caption(item[:70])


def render_hero():
    title_col, action_col = st.columns([4, 1])

    with action_col:
        st.write("")
        st.write("")
        if st.button("Log out", use_container_width=True, key="main_logout"):
            auth.logout()

    with title_col:
        st.markdown(
            """
<div class="viaai-kicker">ViaAI travel planner</div>
<div class="viaai-title">Plan your trip with AI agents</div>
<div class="viaai-subtitle">
Describe the trip you want. ViaAI will search flights, compare hotel context,
build an itinerary, and produce a clean final plan.
</div>
""",
            unsafe_allow_html=True,
        )

def render_quick_prompts():
    cols = st.columns(len(QUICK_PROMPTS))
    for col, (label, value) in zip(cols, QUICK_PROMPTS.items()):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.query = value


def render_plan_input():
    st.markdown('<div class="section-label">Plan Builder</div>', unsafe_allow_html=True)
    user_query = st.text_area(
        "Travel Query",
        value=st.session_state.query,
        placeholder="Plan a 7-day Japan trip including flights, hotels, sightseeing, and budget...",
        height=130,
        label_visibility="collapsed",
    )
    st.session_state.query = user_query

    generate = st.button(
        "Generate Travel Plan",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.running,
    )

    return user_query, generate


def render_agent_update(update):
    with st.status(
        f"{update['title']}",
        expanded=True,
        state="complete",
    ):
        st.caption(update["subtitle"])
        if update["content"]:
            st.markdown(update["content"])
        else:
            st.info(update["empty_message"])


def render_metrics(llm_calls):
    st.markdown("---")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
<div class="metric-box">
    <div class="metric-value">4</div>
    <div class="metric-label">Agents</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
<div class="metric-box">
    <div class="metric-value">{llm_calls}</div>
    <div class="metric-label">LLM Calls</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
<div class="metric-box">
    <div class="metric-value">Done</div>
    <div class="metric-label">Status</div>
</div>
""",
            unsafe_allow_html=True,
        )


def render_final_plan(final_response):
    if not final_response:
        return

    st.markdown("---")
    st.markdown("## Final Travel Plan")
    st.markdown('<div class="final-wrap">', unsafe_allow_html=True)
    st.markdown(final_response)
    st.markdown("</div>", unsafe_allow_html=True)


def render_download(file_content, filename, saved_path):
    st.download_button(
        "Download Plan",
        data=file_content,
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )
    st.success(f"Saved to {saved_path}")
