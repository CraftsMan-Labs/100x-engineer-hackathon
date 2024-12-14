import streamlit as st
from database import save_report, get_user_reports, get_user_products
from api_code import competition_analyse
import json

def show_competition_analysis_page():
    st.header("Competition Analysis")
    
    # Show existing reports in an expander
    with st.expander("View Previous Competition Analysis Reports"):
        reports = get_user_reports(st.session_state.email)
        competition_reports = [r for r in reports if r[0] == "competition_analysis"]
        
        if competition_reports:
            report = competition_reports[0]  # Get most recent report
            st.subheader(f"{report[2]} ({report[3]})")
            st.json(json.loads(report[1]))
        else:
            st.info("No previous competition analysis reports found.")
    
    # Get available products
    products = get_user_products(st.session_state.email)
    
    if not products:
        st.warning("Please add your product details first!")
        return
        
    st.subheader("New Competition Analysis")
    
    # Create product selection dropdown
    product_options = {f"{p[1]} ({p[3]})": p for p in products}  # p[1] is name, p[3] is domain
    selected_product_name = st.selectbox(
        "Select Product for Analysis",
        options=list(product_options.keys()),
        help="Choose which product to analyze"
    )
    
    # Get selected product details
    selected_product = product_options[selected_product_name]
    product_name = selected_product[1]  # name is at index 1
    product_description = selected_product[2]  # description is at index 2
    
    st.info(f"Selected product details:\nName: {product_name}\nDescription: {product_description}")
    
    if st.button("Analyze Competition"):
        
        try:
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
        else:
            st.info("Click 'Analyze Competition' to start the analysis")
