import secrets
from urllib.parse import urlencode

import requests
import streamlit as st


def _auth_secret_is_set(value):
    if not value:
        return False

    text = str(value).strip()
    return bool(text) and not text.startswith("CHANGE_ME")


def is_auth_configured():
    try:
        auth = st.secrets.get("auth", {})
    except Exception:
        return False

    required = (
        "redirect_uri",
        "cookie_secret",
        "client_id",
        "client_secret",
        "server_metadata_url",
    )

    return all(_auth_secret_is_set(auth.get(key)) for key in required)


def get_auth_config():
    auth = st.secrets.get("auth", {})

    return {
        "redirect_uri": auth.get("redirect_uri", "http://localhost:8501"),
        "client_id": auth.get("client_id"),
        "client_secret": auth.get("client_secret"),
        "server_metadata_url": auth.get("server_metadata_url"),
        "scope": auth.get("client_kwargs", {}).get("scope", "profile email"),
    }


@st.cache_data(ttl=3600)
def load_provider_metadata(server_metadata_url):
    response = requests.get(server_metadata_url, timeout=10)
    response.raise_for_status()
    return response.json()


def normalize_userinfo(userinfo):
    email = (
        userinfo.get("email")
        or userinfo.get("email_address")
        or userinfo.get("primary_email_address")
    )
    name = (
        userinfo.get("name")
        or userinfo.get("full_name")
        or userinfo.get("username")
        or email
    )
    user_id = userinfo.get("sub") or userinfo.get("id") or email

    return {
        "id": user_id,
        "email": email,
        "name": name,
        "raw": userinfo,
    }


def exchange_code_for_user(code):
    auth = get_auth_config()
    metadata = load_provider_metadata(auth["server_metadata_url"])

    token_response = requests.post(
        metadata["token_endpoint"],
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": auth["redirect_uri"],
        },
        auth=(auth["client_id"], auth["client_secret"]),
        timeout=15,
    )
    token_response.raise_for_status()
    token = token_response.json()

    access_token = token.get("access_token")
    if not access_token:
        raise ValueError("Clerk did not return an access token.")

    userinfo_endpoint = metadata.get("userinfo_endpoint")
    if not userinfo_endpoint:
        raise ValueError("Clerk metadata does not include a userinfo endpoint.")

    user_response = requests.get(
        userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    user_response.raise_for_status()

    return normalize_userinfo(user_response.json())


def build_login_url():
    auth = get_auth_config()
    metadata = load_provider_metadata(auth["server_metadata_url"])
    state = secrets.token_urlsafe(24)
    st.session_state.oauth_state = state

    query = urlencode(
        {
            "client_id": auth["client_id"],
            "redirect_uri": auth["redirect_uri"],
            "response_type": "code",
            "scope": auth["scope"],
            "state": state,
        }
    )

    return f"{metadata['authorization_endpoint']}?{query}"


def handle_oauth_callback():
    params = st.query_params
    error = params.get("error")

    if error:
        description = params.get("error_description", error)
        st.error(f"Clerk login failed: {description}")
        st.query_params.clear()
        st.stop()

    code = params.get("code")
    if not code:
        return

    expected_state = st.session_state.get("oauth_state")
    returned_state = params.get("state")

    if expected_state and returned_state and expected_state != returned_state:
        st.error("Clerk login failed because the OAuth state did not match.")
        st.query_params.clear()
        st.stop()

    try:
        st.session_state.auth_user = exchange_code_for_user(code)
    except Exception as exc:
        st.error(f"Clerk login callback failed: {exc}")
        st.stop()

    st.session_state.pop("oauth_state", None)
    st.query_params.clear()
    st.rerun()


def logout():
    st.session_state.pop("auth_user", None)
    st.session_state.pop("oauth_state", None)
    st.query_params.clear()
    st.rerun()


def user_value(*keys):
    user = st.session_state.get("auth_user")

    if user is None:
        return None

    for key in keys:
        value = None

        if hasattr(user, "get"):
            try:
                value = user.get(key)
            except Exception:
                value = None

        if value is None:
            value = getattr(user, key, None)

        if value:
            return value

    return None


def user_is_logged_in():
    return bool(st.session_state.get("auth_user", {}).get("id"))
