import streamlit as st
from database import save_report, get_user_reports
import json

def show_customer_product_page():
    st.header("Product Details Management")
    
    # Get existing product details if any
    product_reports = get_user_reports(st.session_state.email, "product_details")
    
    current_details = {}
    if product_reports:
        report = product_reports[0]  # Most recent report
        current_details = {
            "product_name": report[2],
            "product_description": json.loads(report[1]).get("product_description", ""),
            "domain": report[3],
            "offerings": report[4]
        }
    
    with st.form("product_details_form"):
        product_name = st.text_input(
            "Product Name", 
            value=current_details.get("product_name", "")
        )
        
        product_description = st.text_area(
            "Product Description",
            value=current_details.get("product_description", ""),
            help="Provide a detailed description of your product"
        )
        
        domain = st.text_input(
            "Domain",
            value=current_details.get("domain", ""),
            help="e.g., Edutech, FinTech, HealthTech"
        )
        
        offerings = st.text_area(
            "Product Offerings",
            value=current_details.get("offerings", ""),
            help="List the key features and services your product offers"
        )
        
        submitted = st.form_submit_button("Save Product Details")
        
        if submitted and all([product_name, product_description, domain, offerings]):
            product_data = {
                "product_name": product_name,
                "product_description": product_description,
                "domain": domain,
                "offerings": offerings
            }
            
            # Save to database
            save_report(
                st.session_state.email,
                "product_details",
                json.dumps(product_data),
                product_name,
                domain,
                offerings
            )
            
            st.success("Product details saved successfully!")
            
        elif submitted:
            st.warning("Please fill in all fields")
