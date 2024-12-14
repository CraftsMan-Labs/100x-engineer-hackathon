import streamlit as st
from database import save_report, get_user_reports
from api_code import market_expansion
import json

def show_market_expansion_page():
    st.header("Market Expansion Analysis")
    
    # Show latest report in an expander
    reports = get_user_reports(st.session_state.email)
    expansion_reports = [r for r in reports if r[0] == "market_expansion"]
    
    if expansion_reports:
        with st.expander("View Latest Market Expansion Report", expanded=True):
            latest_report = expansion_reports[0]  # Get most recent report
            st.subheader(f"{latest_report[2]} ({latest_report[3]})")
            st.json(json.loads(latest_report[1]))
    
    st.subheader("New Market Expansion Analysis")
    
    # Get user's existing reports for analysis
    reports = get_user_reports(st.session_state.email)
    market_reports = [r for r in reports if r[0] == "market_analysis"]
    customer_reports = [r for r in reports if r[0] == "customer_discovery"]
    
    if not market_reports or not customer_reports:
        st.warning("Please complete Market Analysis and Customer Discovery first!")
        return
    
    # Create selection boxes for reports
    selected_market = st.selectbox(
        "Select Market Analysis Report",
        options=[(r[2], r[1]) for r in market_reports],
        format_func=lambda x: x[0]
    )
    
    selected_customer = st.selectbox(
        "Select Customer Discovery Report",
        options=[(r[2], r[1]) for r in customer_reports],
        format_func=lambda x: x[0]
    )
    
    domain = st.text_input("Target Domain for Expansion")
    
    if st.button("Analyze Expansion Opportunities") and domain:
        with st.spinner("Analyzing expansion opportunities..."):
            try:
                market_report = json.loads(selected_market[1])
                customer_report = json.loads(selected_customer[1])
                
                response = market_expansion(domain, market_report, customer_report)
                response_data = json.loads(response)
                
                # Display results
                st.subheader("Expansion Analysis Results")
                st.json(response_data)
                
                # Save report
                save_report(
                    st.session_state.email,
                    "market_expansion",
                    response,
                    f"Market Expansion - {domain}"
                )
                
                st.success("Analysis complete and saved!")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
