import streamlit as st
from database import save_report, get_user_reports, get_user_products
from api_code import market_expansion
import json

def json_to_markdown(data: dict) -> str:
    """Convert market expansion JSON response to readable markdown"""
    markdown = []
    
    # Primary Domain
    if "primary_domain" in data:
        markdown.append(f"## Primary Domain\n{data['primary_domain']}")
    
    # Expansion Domains
    if "expansion_domains" in data:
        markdown.append("\n## Expansion Domains")
        for domain in data["expansion_domains"]:
            markdown.append(f"- {domain}")
    
    # Strategic Rationale
    if "strategic_rationale" in data:
        markdown.append("\n## Strategic Rationale")
        for key, value in data["strategic_rationale"].items():
            markdown.append(f"\n### {key.replace('_', ' ').title()}")
            markdown.append(value)
    
    # Competitive Landscape
    if "competitive_landscape" in data:
        markdown.append("\n## Competitive Landscape")
        for key, value in data["competitive_landscape"].items():
            markdown.append(f"\n### {key.replace('_', ' ').title()}")
            markdown.append(value)
    
    # Investment Requirements
    if "investment_requirements" in data:
        markdown.append("\n## Investment Requirements")
        for key, value in data["investment_requirements"].items():
            markdown.append(f"- **{key.replace('_', ' ').title()}**: ${value:,}")
    
    # Risk Assessment
    if "risk_assessment" in data:
        markdown.append("\n## Risk Assessment")
        for key, value in data["risk_assessment"].items():
            markdown.append(f"- **{key.replace('_', ' ').title()}**: {value:.2f}")
    
    # Potential Synergies
    if "potential_synergies" in data:
        markdown.append("\n## Potential Synergies")
        for synergy in data["potential_synergies"]:
            markdown.append(f"- {synergy}")
    
    return "\n".join(markdown)

def show_market_expansion_page():
    st.header("Market Expansion Analysis")
    
    # Show latest report in an expander
    reports = get_user_reports(st.session_state.email)
    expansion_reports = [r for r in reports if r[0] == "market_expansion"]
    
    if expansion_reports:
        with st.expander("View Latest Market Expansion Report", expanded=True):
            latest_report = expansion_reports[0]  # Get most recent report
            st.subheader(f"{latest_report[2]} ({latest_report[3]})")
            report_data = json.loads(latest_report[1])
            st.markdown(json_to_markdown(report_data))
    
    st.subheader("New Market Expansion Analysis")
    
    # Get available products
    products = get_user_products(st.session_state.email)
    
    if not products:
        st.warning("Please add your product details first!")
        return
        
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
    domain = selected_product[3]  # domain is at index 3
    
    st.info(f"Selected product details:\nName: {product_name}\nDomain: {domain}")
    
    # Get user's existing reports for analysis
    reports = get_user_reports(st.session_state.email)
    market_reports = [r for r in reports if r[0] == "market_analysis"]
    customer_reports = [r for r in reports if r[0] == "customer_discovery"]
    
    if not market_reports or not customer_reports:
        st.warning("Please complete Market Analysis and Customer Discovery first!")
        return
    
    # Create selection boxes for reports
    selected_market = st.selectbox(
        "Select Market Analysis Report",
        options=[(r[2], r[1]) for r in market_reports],
        format_func=lambda x: x[0]
    )
    
    selected_customer = st.selectbox(
        "Select Customer Discovery Report",
        options=[(r[2], r[1]) for r in customer_reports],
        format_func=lambda x: x[0]
    )
    
    if st.button("Analyze Expansion Opportunities"):
        with st.spinner("Analyzing expansion opportunities..."):
            try:
                market_report = json.loads(selected_market[1])
                customer_report = json.loads(selected_customer[1])
                
                response = market_expansion(domain, market_report, customer_report)
                response_data = json.loads(response)
                
                # Display results using markdown
                st.markdown(json_to_markdown(response_data))
                
                # Save report
                save_report(
                    st.session_state.email,
                    "market_expansion",
                    response,
                    f"Market Expansion - {product_name}"
                )
                
                st.success("Analysis complete and saved!")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
