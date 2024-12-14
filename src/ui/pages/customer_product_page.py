import streamlit as st
import pandas as pd
from database import save_product, get_user_products

def show_customer_product_page():
    st.header("Product Details Management")
    
    st.subheader("Your Current Products")
    
    # Get existing products
    products = get_user_products(st.session_state.email)
    
    # Display existing products in a table
    if products:
        product_df = pd.DataFrame(
            products,
            columns=['ID', 'Product Name', 'Description', 'Domain', 'Offerings', 'Created At']
        )
        
        # Display each product in an expander for better readability
        for _, row in product_df.iterrows():
            with st.expander(f"📦 {row['Product Name']} ({row['Created At']})"):
                st.write("**Product Description:**")
                st.write(row['Description'])
                st.write("**Domain:**", row['Domain'])
                st.write("**Offerings:**", row['Offerings'])
                st.divider()
    else:
        st.info("No products added yet. Use the form below to add your first product!")
    
    st.subheader("Add New Product")
    with st.form("product_details_form"):
        product_name = st.text_input(
            "Product Name",
            help="Enter your product name"
        )
        
        product_description = st.text_area(
            "Product Description",
            help="Provide a detailed description of your product"
        )
        
        domain = st.text_input(
            "Domain",
            help="e.g., Edutech, FinTech, HealthTech"
        )
        
        offerings = st.text_area(
            "Product Offerings",
            help="List the key features and services your product offers"
        )
        
        submitted = st.form_submit_button("Save Product Details")
        
        if submitted and all([product_name, product_description, domain, offerings]):
            # Save to database
            if save_product(
                st.session_state.email,
                product_name,
                product_description,
                domain,
                offerings
            ):
                st.success("Product details saved successfully!")
                st.rerun()  # Refresh the page to show the new product
            else:
                st.error("Failed to save product details")
            
            st.success("Product details saved successfully!")
            
        elif submitted:
            st.warning("Please fill in all fields")
