import streamlit as st
from database import save_report, get_user_reports
from api_code import market_analysis, img_b64_str_to_pil_image
import json

def show_market_analysis_page():
    st.header("Market Analysis")
    
    # Show existing reports in an expander
    with st.expander("View Previous Market Analysis Reports"):
        reports = get_user_reports(st.session_state.email)
        market_reports = [r for r in reports if r[0] == "market_analysis"]
        
        if market_reports:
            report = market_reports[0]  # Get most recent report
            st.subheader(f"{report[2]} ({report[3]})")
            st.json(json.loads(report[1]))
        else:
            st.info("No previous market analysis reports found.")
    
    st.subheader("New Market Analysis")
    
    # Get product details
    product_reports = get_user_reports(st.session_state.email, "product_details")
    
    if not product_reports:
        st.warning("Please add your product details first!")
        return
        
    # Get latest product details
    latest_product = product_reports[0]
    domain = latest_product[3]  # domain is at index 3
    offerings = latest_product[4]  # offerings is at index 4
    
    st.info(f"Using product details:\nDomain: {domain}\nOfferings: {offerings}")
    
    if st.button("Generate Analysis"):
            with st.spinner("Analyzing market..."):
                try:
                    response = market_analysis(offerings, domain)
                    response_data = json.loads(response)
                    
                    # Display results
                    st.subheader("Analysis Results")
                    st.json(response_data)
                    
                    # Save report
                    save_report(
                        st.session_state.email,
                        "market_analysis",
                        response,
                        f"Market Analysis - {domain}"
                    )
                    
                    st.success("Analysis complete and saved!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
