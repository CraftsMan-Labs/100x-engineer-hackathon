import streamlit as st
from database import save_report
from api_code import customer_discovery
import json

def show_customer_discovery_page():
    st.header("Customer Discovery")
    
    with st.form("customer_discovery_form"):
        product_name = st.text_input("Product Name")
        product_description = st.text_area("Product Description")
        domain = st.text_input("Domain")
        offerings = st.text_area("Offerings")
        
        submitted = st.form_submit_button("Discover Customer Segments")
        
        if submitted and all([product_name, product_description, domain, offerings]):
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
            
        elif submitted:
            st.warning("Please fill in all fields")
