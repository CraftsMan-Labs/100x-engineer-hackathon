import streamlit as st
from database import save_report
from api_code import competition_analyse
import json

def show_competition_analysis_page():
    st.header("Competition Analysis")
    
    with st.form("competition_analysis_form"):
        product_name = st.text_input("Product Name")
        product_description = st.text_area("Product Description")
        
        submitted = st.form_submit_button("Analyze Competition")
        
        if submitted and product_name and product_description:
            with st.spinner("Analyzing competition..."):
                try:
                    response = competition_analyse(product_name, product_description)
                    response_data = json.loads(response)
                    
                    # Display results
                    st.subheader("Competition Analysis Results")
                    st.json(response_data)
                    
                    # Save report
                    save_report(
                        st.session_state.email,
                        "competition_analysis",
                        response,
                        product_name
                    )
                    
                    st.success("Analysis complete and saved!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
