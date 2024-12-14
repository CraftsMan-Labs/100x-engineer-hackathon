import streamlit as st
from database import save_report, get_user_reports
from api_code import product_evolution
import json

def json_to_markdown(data: dict) -> str:
    """Convert product evolution JSON response to readable markdown"""
    markdown = []
    
    # Strategy Section
    if "strategy" in data:
        strategy = data["strategy"]
        markdown.append("## Product Evolution Strategy")
        markdown.append(f"\n**Primary Domain:** {strategy.get('primary_domain', 'N/A')}")
        
        if "phases" in strategy:
            markdown.append("\n### Development Phases")
            for phase in strategy["phases"]:
                markdown.append(f"\n#### Phase {phase.get('phase_number', 'N/A')}: {phase.get('name', 'Unnamed Phase')}")
                markdown.append(f"\n{phase.get('description', '')}")
                
                if "target_customer_segments" in phase:
                    markdown.append("\n**Target Customer Segments:**")
                    for segment in phase["target_customer_segments"]:
                        markdown.append(f"- {segment}")
                
                if "key_features" in phase:
                    markdown.append("\n**Key Features:**")
                    for feature in phase["key_features"]:
                        markdown.append(f"- {feature}")
                
                if "value_proposition" in phase:
                    markdown.append(f"\n**Value Proposition:**\n{phase['value_proposition']}")
                
                if "expected_market_reaction" in phase:
                    markdown.append(f"\n**Expected Market Reaction:**\n{phase['expected_market_reaction']}")
                
                if "success_metrics" in phase:
                    markdown.append("\n**Success Metrics:**")
                    for metric in phase["success_metrics"]:
                        markdown.append(f"- {metric}")
                
                if "risk_mitigation_strategies" in phase:
                    markdown.append("\n**Risk Mitigation Strategies:**")
                    for strategy in phase["risk_mitigation_strategies"]:
                        markdown.append(f"- {strategy}")
        
        if "overall_vision" in strategy:
            markdown.append("\n### Overall Vision")
            markdown.append(strategy["overall_vision"])
        
        if "long_term_goals" in strategy:
            markdown.append("\n### Long-term Goals")
            for goal in strategy["long_term_goals"]:
                markdown.append(f"- {goal}")
        
        if "competitive_differentiation" in strategy:
            markdown.append("\n### Competitive Differentiation")
            for diff in strategy["competitive_differentiation"]:
                markdown.append(f"- {diff}")
        
        if "user_adoption_trend" in strategy:
            trend = strategy["user_adoption_trend"]
            markdown.append("\n### User Adoption Analysis")
            markdown.append(f"\n**Reasoning:**\n{trend.get('reasoning', '')}")
            
            if "key_insights" in trend:
                markdown.append("\n**Key Insights:**")
                for insight in trend["key_insights"]:
                    markdown.append(f"- {insight}")
    
    # Visuals Section
    if "visuals" in data and "img" in data["visuals"]:
        markdown.append("\n### Visualization")
        img_base64 = data["visuals"]["img"]
        markdown.append(f'\n![Growth Trend](data:image/png;base64,{img_base64})')
    
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
