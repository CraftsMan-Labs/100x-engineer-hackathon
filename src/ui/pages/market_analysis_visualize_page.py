import streamlit as st
from database import save_report, get_user_reports, get_user_products
from api_code import market_analysis_visualise, img_b64_str_to_pil_image
import json

def json_to_markdown(data: dict) -> str:
    """Convert market analysis visualization JSON response to readable markdown"""
    markdown = []
    
    # Add visualization image if present
    if "img" in data:
        markdown.append("## Market Trend Visualization")
        
    # Add metadata if present
    if "metadata" in data:
        metadata = data["metadata"]
        markdown.append("\n## Analysis Metadata")
        if "title" in metadata:
            markdown.append(f"\n### {metadata['title']}")
        
        markdown.append("\n**Analysis Details:**")
        markdown.append(f"- **Date Generated:** {metadata['date_generated'][:10]}")
        markdown.append(f"- **X-Axis:** {metadata['x_axis_label']}")
        markdown.append(f"- **Y-Axis:** {metadata['y_axis_label']}")
        
        if "metrics" in metadata:
            markdown.append("\n**Tracked Metrics:**")
            for metric in metadata["metrics"]:
                markdown.append(f"- {metric}")
    
    # Add reason if present
    if "reason" in data:
        markdown.append(f"\n### Analysis Reason\n{data['reason']}")
    
    # Add insights if present
    if "insights" in data:
        markdown.append("\n### Key Insights")
        for insight in data["insights"]:
            markdown.append(f"- {insight}")
            
    return "\n".join(markdown)

def show_market_analysis_visualize_page():
    st.header("Market Analysis Visualization")
    
    # Show existing reports in an expander
    with st.expander("View Previous Market Visualizations"):
        reports = get_user_reports(st.session_state.email)
        visual_reports = [r for r in reports if r[0] == "market_visualization"]
        
        if visual_reports:
            report = visual_reports[0]  # Get most recent report
            st.subheader(f"{report[2]} ({report[3]})")
            report_json = json.loads(report[1])
            if "img" in report_json:
                st.image(img_b64_str_to_pil_image(report_json["img"]))
            st.markdown(json_to_markdown(report_json))
        else:
            st.info("No previous market visualizations found.")
    
    st.subheader("New Market Visualization")
    
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
    domain = selected_product[3]  # domain is at index 3
    offerings = selected_product[4]  # offerings is at index 4
    
    st.info(f"Selected product details:\nDomain: {domain}\nOfferings: {offerings}")
    
    if st.button("Generate Visualization"):
            with st.spinner("Generating visualization..."):
                try:
                    response = market_analysis_visualise(offerings, domain)
                    response_data = json.loads(response)
                    
                    # Display visualization
                    if "img" in response_data:
                        st.image(img_b64_str_to_pil_image(response_data["img"]))
                    
                    # Display insights
                    if "insights" in response_data:
                        st.subheader("Key Insights")
                        for insight in response_data["insights"]:
                            st.write(f"• {insight}")
                    
                    # Display metadata
                    if "metadata" in response_data:
                        st.subheader("Analysis Metadata")
                        st.json(response_data["metadata"])
                    
                    # Save report
                    save_report(
                        st.session_state.email,
                        "market_visualization",
                        json.dumps(response_data),
                        f"Market Visualization - {domain}"
                    )
                    
                    st.success("Visualization generated and saved!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
