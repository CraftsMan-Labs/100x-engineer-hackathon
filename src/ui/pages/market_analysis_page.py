import streamlit as st
from database import save_report
from api_code import market_analysis, img_b64_str_to_pil_image
import json

def show_market_analysis_page():
    st.header("Market Analysis")
    
    with st.form("market_analysis_form"):
        domain = st.text_input("Domain")
        offerings = st.text_area("Offerings")
        
        submitted = st.form_submit_button("Generate Analysis")
        
        if submitted and domain and offerings:
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
