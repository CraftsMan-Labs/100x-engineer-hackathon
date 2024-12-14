import streamlit as st
from database import save_report, get_user_reports, get_user_products
from api_code import customer_discovery
import json

def show_customer_discovery_page():
    st.header("Customer Discovery")
    
    # Show existing reports in an expander
    with st.expander("View Previous Customer Discovery Reports"):
        reports = get_user_reports(st.session_state.email)
        customer_reports = [r for r in reports if r[0] == "customer_discovery"]
        
        if customer_reports:
            report = customer_reports[0]  # Get most recent report
            st.subheader(f"{report[2]} ({report[3]})")
            st.json(json.loads(report[1]))
        else:
            st.info("No previous customer discovery reports found.")
    
    # Get available products
    products = get_user_products(st.session_state.email)
    
    if not products:
        st.warning("Please add your product details first!")
        return
        
    st.subheader("New Customer Discovery")
    
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
    domain = selected_product[3]  # domain is at index 3
    offerings = selected_product[4]  # offerings is at index 4
    
    st.info(f"Selected product details:\nName: {product_name}\nDescription: {product_description}\nDomain: {domain}\nOfferings: {offerings}")
    
    if st.button("Discover Customer Segments"):
        if all([product_name, product_description, domain, offerings]):
            with st.spinner("Analyzing customer segments..."):
                try:
                    response = customer_discovery(
                        product_name,
                        product_description,
                        domain,
                        offerings
                    )
                    response_data = json.loads(response)
                    
                    # Display results
                    st.subheader("Customer Discovery Results")
                    
                    # Display market size
                    st.metric("Total Market Size", response_data.get("total_market_size", "N/A"))
                    
                    # Display niches
                    if "niches" in response_data:
                        st.subheader("Market Niches")
                        for niche in response_data["niches"]:
                            with st.expander(f"{niche['name']} - Market Size: {niche['market_size']}"):
                                st.write(f"Description: {niche['description']}")
                                st.write(f"Growth Potential: {niche['growth_potential']}")
                                st.write("Key Characteristics:")
                                for char in niche['key_characteristics']:
                                    st.write(f"• {char}")
                    
                    # Save report
                    save_report(
                        st.session_state.email,
                        "customer_discovery",
                        response,
                        product_name
                    )
                    
                    st.success("Analysis complete and saved!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
