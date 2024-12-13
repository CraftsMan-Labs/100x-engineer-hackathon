import streamlit as st
from database import save_report, get_user_reports
from api_code import product_evolution
import json

def show_product_evolution_page():
    st.header("Product Evolution Analysis")
    
    # Get user's existing reports
    reports = get_user_reports(st.session_state.email)
    market_reports = [r for r in reports if r[0] == "market_analysis"]
    customer_reports = [r for r in reports if r[0] == "customer_discovery"]
    expansion_reports = [r for r in reports if r[0] == "market_expansion"]
    
    if not all([market_reports, customer_reports, expansion_reports]):
        st.warning("Please complete Market Analysis, Customer Discovery, and Market Expansion first!")
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
    
    selected_expansion = st.selectbox(
        "Select Market Expansion Report",
        options=[(r[2], r[1]) for r in expansion_reports],
        format_func=lambda x: x[0]
    )
    
    if st.button("Generate Evolution Strategy"):
        with st.spinner("Analyzing product evolution opportunities..."):
            try:
                market_report = json.loads(selected_market[1])
                customer_report = json.loads(selected_customer[1])
                expansion_report = json.loads(selected_expansion[1])
                
                response = product_evolution(market_report, customer_report, expansion_report)
                response_data = json.loads(response)
                
                # Display results
                st.subheader("Product Evolution Strategy")
                st.json(response_data)
                
                # Save report
                save_report(
                    st.session_state.email,
                    "product_evolution",
                    response,
                    f"Product Evolution - {selected_market[0]}"
                )
                
                st.success("Evolution strategy generated and saved!")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
