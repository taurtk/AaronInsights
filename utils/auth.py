import streamlit as st
import hmac

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            return st.form_submit_button("Log in")

    if st.session_state.get('authenticated'):
        return True

    # Show inputs for username + password.
    st.title("🔐 Welcome to Aaron's AI Idea Generator")
    if login_form():
        if (
            st.session_state['username'].strip() == 'aaron'
            and hmac.compare_digest(st.session_state['password'], '@321')
        ):
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("😕 Invalid username or password")
            return False
    return False
