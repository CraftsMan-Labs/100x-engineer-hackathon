import streamlit as st
from database import save_report, get_user_reports, get_user_products
from api_code import competition_analyse
import json

def json_to_markdown(data: dict) -> str:
    """Convert competition analysis JSON response to readable markdown"""
    markdown = []
    
    # Product Name
    if "product_name" in data:
        markdown.append(f"# Competition Analysis for {data['product_name']}")
    
    # Competitors Section
    if "competitors" in data:
        markdown.append("\n## Key Competitors")
        for comp in data["competitors"]:
            markdown.append(f"\n### {comp['name']}")
            markdown.append(f"\n{comp['description']}")
            
            if "main_products" in comp:
                markdown.append("\n**Main Products:**")
                for product in comp["main_products"]:
                    markdown.append(f"- {product}")
            
            if "target_market" in comp:
                markdown.append(f"\n**Target Market:** {comp['target_market']}")
            
            if "key_differentiators" in comp:
                markdown.append("\n**Key Differentiators:**")
                for diff in comp["key_differentiators"]:
                    markdown.append(f"- {diff}")
            
            markdown.append("\n")  # Add spacing between competitors
    
    # Derivatives Section
    if "derivatives" in data:
        markdown.append("\n## Potential Product Derivatives")
        for deriv in data["derivatives"]:
            markdown.append(f"\n### {deriv['name']}")
            markdown.append(f"\n{deriv['description']}")
            markdown.append(f"\n**Target Market:** {deriv['target_market']}")
            markdown.append("\n")
    
    return "\n".join(markdown)

def show_competition_analysis_page():
    st.header("Competition Analysis")
    
    # Show existing reports in an expander
    with st.expander("View Previous Competition Analysis Reports"):
        reports = get_user_reports(st.session_state.email)
        competition_reports = [r for r in reports if r[0] == "competition_analysis"]
        
        if competition_reports:
            report = competition_reports[0]  # Get most recent report
            st.subheader(f"{report[2]} ({report[3]})")
            st.markdown(json_to_markdown(json.loads(report[1])))
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
        with st.spinner("Analyzing competition..."):
            try:
                response = competition_analyse(product_name, product_description)
                response_data = json.loads(response)
                
                # Display results using markdown
                st.markdown(json_to_markdown(response_data))
                
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
