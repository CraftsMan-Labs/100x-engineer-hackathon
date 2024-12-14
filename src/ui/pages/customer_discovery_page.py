import streamlit as st
from database import save_report, get_user_reports, get_user_products
from api_code import customer_discovery
import json

def json_to_markdown(data: dict) -> str:
    """Convert customer discovery JSON response to readable markdown"""
    markdown = []
    
    # Primary Domain
    if "primary_domain" in data:
        markdown.append(f"## Primary Domain\n{data['primary_domain']}")
    
    # Total Market Size
    if "total_market_size" in data:
        markdown.append(f"\n## Total Market Size\n${data['total_market_size']:,}")
    
    # Market Niches
    if "niches" in data:
        markdown.append("\n## Market Niches")
        for niche in data["niches"]:
            markdown.append(f"\n{niche['name']}")
            markdown.append(f"\nMarket Size: ${niche['market_size']:,}")
            markdown.append(f"\nGrowth Potential: {niche['growth_potential']*100:.1f}%")
            
            if "key_characteristics" in niche:
                markdown.append("\n**Key Characteristics:**")
                for char in niche["key_characteristics"]:
                    markdown.append(f"- {char}")
            markdown.append("\n")  # Add spacing between niches
    
    # Ideal Customer Profile
    if "ideal_customer_profile" in data and "insights" in data["ideal_customer_profile"]:
        markdown.append("\n## Ideal Customer Profile")
        markdown.append(data["ideal_customer_profile"]["insights"])
    
    # Investor Sentiment
    if "investor_sentiment" in data and "insights" in data["investor_sentiment"]:
        markdown.append("\n## Investor Sentiment")
        markdown.append(data["investor_sentiment"]["insights"])
    
    return "\n".join(markdown)

def show_customer_discovery_page():
    st.header("Customer Discovery")
    
    # Show existing reports in an expander
    with st.expander("View Previous Customer Discovery Reports"):
        reports = get_user_reports(st.session_state.email)
        customer_reports = [r for r in reports if r[0] == "customer_discovery"]
        
        if customer_reports:
            report = customer_reports[0]  # Get most recent report
            st.subheader(f"{report[2]} ({report[3]})")
            st.markdown(json_to_markdown(json.loads(report[1])))
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
                    
                    # Display results using markdown
                    st.markdown(json_to_markdown(response_data))
                    
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
