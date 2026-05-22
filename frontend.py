import os

import streamlit as st

from services.plan_export import build_plan_markdown, save_plan
from services.travel_runner import (
    collect_update,
    empty_collected_results,
    stream_travel_plan,
)
from ui import auth
from ui.components import (
    render_agent_update,
    render_download,
    render_final_plan,
    render_hero,
    render_metrics,
    render_plan_input,
    render_quick_prompts,
    render_sidebar,
    show_login_screen,
)
from ui.styles import apply_styles


def init_session_state():
    defaults = {
        "query": "",
        "history": [],
        "running": False,
        "dark_theme": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_signed_in_context():
    thread_id = auth.user_value("sub", "id", "user_id")
    signed_in_email = auth.user_value("email", "email_address")
    signed_in_name = auth.user_value("name", "full_name", "username", "given_name")

    if not thread_id:
        st.error("Clerk login succeeded, but no user ID or email was returned.")
        st.stop()

    return thread_id, signed_in_email, signed_in_name


def run_generation(user_query, thread_id, user_label):
    final_query = user_query.strip()
    if not final_query:
        st.warning("Please enter your travel query.")
        st.stop()

    st.session_state.running = True
    if final_query not in st.session_state.history:
        st.session_state.history.append(final_query)

    collected = empty_collected_results()

    st.markdown("---")
    st.markdown("## Agent Progress")

    try:
        for update in stream_travel_plan(final_query, thread_id):
            collect_update(collected, update)
            render_agent_update(update)
    except Exception as exc:
        st.error(f"ViaAI could not generate this travel plan: {exc}")
        st.stop()
    finally:
        st.session_state.running = False

    render_metrics(collected["llm_calls"])
    render_final_plan(collected["final_response"])

    file_content = build_plan_markdown(user_label, final_query, collected)
    filename, saved_path = save_plan(file_content, os.path.dirname(__file__))
    render_download(file_content, filename, saved_path)


def main():
    st.set_page_config(
        page_title="ViaAI - Travel Planner",
        page_icon="V",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()
    apply_styles(st.session_state.dark_theme)
    auth.handle_oauth_callback()

    if not auth.user_is_logged_in():
        show_login_screen()

    thread_id, signed_in_email, signed_in_name = get_signed_in_context()
    user_label = signed_in_email or signed_in_name or thread_id

    render_sidebar(
        thread_id=thread_id,
        signed_in_name=signed_in_name,
        signed_in_email=signed_in_email,
        history=st.session_state.history,
    )

    render_hero()
    render_quick_prompts()
    st.markdown("---")

    user_query, generate = render_plan_input()
    if generate:
        run_generation(user_query, thread_id, user_label)


if __name__ == "__main__":
    main()
