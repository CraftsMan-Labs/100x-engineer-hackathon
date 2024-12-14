import streamlit as st
from database import save_report, get_user_reports
from api_code import product_evolution
import json

def json_to_markdown(data: dict) -> str:
    """Convert product evolution JSON response to readable markdown"""
    markdown = []
    
    # Customer Report Section
    if "customer_report" in data:
        markdown.append("## Customer Analysis")
        cr = data["customer_report"]
        markdown.append(f"**Primary Domain:** {cr.get('primary_domain', 'N/A')}")
        markdown.append(f"**Total Market Size:** {cr.get('total_market_size', 'N/A')}")
        
        if "niches" in cr:
            markdown.append("\n### Market Niches")
            for niche in cr["niches"]:
                markdown.append(f"\n#### {niche.get('name', 'Unnamed Niche')}")
                markdown.append(f"- Description: {niche.get('description', 'N/A')}")
                markdown.append(f"- Market Size: {niche.get('market_size', 'N/A')}")
                markdown.append(f"- Growth Potential: {niche.get('growth_potential', 'N/A')}")
                if "key_characteristics" in niche:
                    markdown.append("\nKey Characteristics:")
                    for char in niche["key_characteristics"]:
                        markdown.append(f"- {char}")
        
        if "ideal_customer_profile" in cr:
            markdown.append("\n### Ideal Customer Profile")
            for key, value in cr["ideal_customer_profile"].items():
                markdown.append(f"- **{key}:** {value}")
        
        if "investor_sentiment" in cr:
            markdown.append("\n### Investor Sentiment")
            for key, value in cr["investor_sentiment"].items():
                markdown.append(f"- **{key}:** {value}")
    
    # Market Report Section
    if "market_report" in data:
        markdown.append("\n## Market Analysis")
        mr = data["market_report"]
        if "problem_breakdown" in mr and "questions" in mr["problem_breakdown"]:
            markdown.append("\n### Key Questions")
            for q in mr["problem_breakdown"]["questions"]:
                markdown.append(f"- {q}")
        
        if "search_results" in mr:
            markdown.append("\n### Market Research Results")
            for category, results in mr["search_results"].items():
                markdown.append(f"\n#### {category}")
                for key, value in results.items():
                    markdown.append(f"- **{key}:** {value}")
        
        if "comprehensive_report" in mr:
            markdown.append("\n### Comprehensive Analysis")
            markdown.append(mr["comprehensive_report"])
    
    # Market Expansion Section
    if "market_expansion" in data:
        markdown.append("\n## Market Expansion Strategy")
        me = data["market_expansion"]
        
        markdown.append(f"\n**Primary Domain:** {me.get('primary_domain', 'N/A')}")
        
        if "expansion_domains" in me:
            markdown.append("\n### Target Expansion Domains")
            for domain in me["expansion_domains"]:
                markdown.append(f"- {domain}")
        
        if "strategic_rationale" in me:
            markdown.append("\n### Strategic Rationale")
            for key, value in me["strategic_rationale"].items():
                markdown.append(f"- **{key}:** {value}")
        
        if "competitive_landscape" in me:
            markdown.append("\n### Competitive Landscape")
            for key, value in me["competitive_landscape"].items():
                markdown.append(f"- **{key}:** {value}")
        
        if "investment_requirements" in me:
            markdown.append("\n### Investment Requirements")
            for category, amount in me["investment_requirements"].items():
                markdown.append(f"- **{category}:** ${amount:,.2f}")
        
        if "risk_assessment" in me:
            markdown.append("\n### Risk Assessment")
            for risk, score in me["risk_assessment"].items():
                markdown.append(f"- **{risk}:** {score}")
        
        if "potential_synergies" in me:
            markdown.append("\n### Potential Synergies")
            for synergy in me["potential_synergies"]:
                markdown.append(f"- {synergy}")
    
    return "\n".join(markdown)

def show_product_evolution_page():
    st.header("Product Evolution Analysis")
    
    # Show latest report in an expander
    reports = get_user_reports(st.session_state.email)
    evolution_reports = [r for r in reports if r[0] == "product_evolution"]
    
    if evolution_reports:
        with st.expander("View Latest Product Evolution Report", expanded=True):
            latest_report = evolution_reports[0]  # Get most recent report
            st.subheader(f"{latest_report[2]} ({latest_report[3]})")
            markdown_content = json_to_markdown(json.loads(latest_report[1]))
            st.markdown(markdown_content)
    
    st.subheader("New Product Evolution Analysis")
    
    # Get user's existing reports for analysis
    reports = get_user_reports(st.session_state.email)
    market_reports = [r for r in reports if r[0] == "market_analysis"]
    customer_reports = [r for r in reports if r[0] == "customer_discovery"]
    expansion_reports = [r for r in reports if r[0] == "market_expansion"]
    
    if not all([market_reports, customer_reports, expansion_reports]):
        st.warning("Please complete Market Analysis, Customer Discovery, and Market Expansion first!")
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
    
    selected_expansion = st.selectbox(
        "Select Market Expansion Report",
        options=[(r[2], r[1]) for r in expansion_reports],
        format_func=lambda x: x[0]
    )
    
    if st.button("Generate Evolution Strategy"):
        with st.spinner("Analyzing product evolution opportunities..."):
            try:
                market_report = json.loads(selected_market[1])
                customer_report = json.loads(selected_customer[1])
                expansion_report = json.loads(selected_expansion[1])
                
                response = product_evolution(market_report, customer_report, expansion_report)
                response_data = json.loads(response)
                
                # Display results
                st.subheader("Product Evolution Strategy")
                markdown_content = json_to_markdown(response_data)
                st.markdown(markdown_content)
                
                # Save report
                save_report(
                    st.session_state.email,
                    "product_evolution",
                    response,
                    f"Product Evolution - {selected_market[0]}"
                )
                
                st.success("Evolution strategy generated and saved!")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
