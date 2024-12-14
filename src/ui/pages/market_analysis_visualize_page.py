import streamlit as st
from database import save_report, get_user_reports
from api_code import market_analysis_visualise, img_b64_str_to_pil_image
import json

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
            st.json(report_json)
        else:
            st.info("No previous market visualizations found.")
    
    st.subheader("New Market Visualization")
    with st.form("market_visualization_form"):
        domain = st.text_input("Domain")
        offerings = st.text_area("Offerings")
        
        submitted = st.form_submit_button("Generate Visualization")
        
        if submitted and domain and offerings:
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
