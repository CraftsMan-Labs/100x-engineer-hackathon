import streamlit as st
from auth import signup, login
from database import init_db, get_user_reports
import json

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "email" not in st.session_state:
        st.session_state.email = None


def auth_page():
    st.title("Market Edge Analyzer")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            success, message = login(email, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.email = email
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    with tab2:
        st.header("Signup")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Signup"):
            if password != confirm_password:
                st.error("Passwords don't match")
            else:
                success, message = signup(email, password)
                if success:
                    st.success(message)
                else:
                    st.error(message)


def main_app():
    st.title(f"Welcome to Market Edge Analyzer, {st.session_state.email}!")

    # Only show sidebar and navigation after authentication
    if st.session_state.authenticated:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.email = None
            st.rerun()

        # Sidebar navigation
        page = st.sidebar.radio(
            "Navigation", 
            ["Market Analysis", "Competition Analysis", "Customer Discovery", 
             "Market Visualization", "Market Expansion", "Product Evolution",
             "Chat", "View Reports"]
        )

        if page == "Market Analysis":
        from pages.market_analysis_page import show_market_analysis_page
        show_market_analysis_page()
    elif page == "Competition Analysis":
        from pages.competition_analysis_page import show_competition_analysis_page
        show_competition_analysis_page()
    elif page == "Customer Discovery":
        from pages.customer_discovery_page import show_customer_discovery_page
        show_customer_discovery_page()
    elif page == "Market Visualization":
        from pages.market_analysis_visualize_page import show_market_analysis_visualize_page
        show_market_analysis_visualize_page()
    elif page == "Market Expansion":
        from pages.market_expansion_page import show_market_expansion_page
        show_market_expansion_page()
    elif page == "Product Evolution":
        from pages.product_evolution_page import show_product_evolution_page
        show_product_evolution_page()
    elif page == "Chat":
        from pages.chat_page import show_chat_page
        show_chat_page()
    else:
        show_reports_page()


def show_reports_page():
    st.header("Your Analysis Reports")
    reports = get_user_reports(st.session_state.email)

    if not reports:
        st.info("No reports found. Start a new analysis to generate reports!")
        return

    for report_type, report_data, product_name, created_at in reports:
        with st.expander(f"{product_name} - {report_type} ({created_at})"):
            st.json(json.loads(report_data))




def main():
    init_db()
    init_session_state()

    if not st.session_state.authenticated:
        auth_page()
    else:
        main_app()


if __name__ == "__main__":
    main()
