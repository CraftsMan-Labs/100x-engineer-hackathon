import streamlit as st
from database import save_report, get_user_reports
import json

def show_customer_product_page():
    st.header("Product Details Management")
    
    # Get existing product details if any
    reports = get_user_reports(st.session_state.email)
    product_reports = [r for r in reports if r[0] == "product_details"]
    
    current_details = {}
    if product_reports:
        current_details = json.loads(product_reports[0][1])
    
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
                product_name
            )
            
            st.success("Product details saved successfully!")
            
        elif submitted:
            st.warning("Please fill in all fields")
