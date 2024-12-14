import streamlit as st
from database import save_report, get_user_reports
from api_code import chat_pro_mode
import json
import matplotlib.pyplot as plt
import numpy as np

def show_god_chat_page():
    st.header("Advanced Market Analysis Chat (God Mode)")
    
    # Chat history
    if "god_messages" not in st.session_state:
        st.session_state.god_messages = []

    # Display chat history
    for message in st.session_state.god_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask advanced market analysis questions..."):
        # Add user message to chat history
        st.session_state.god_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response_data = json.loads(chat_pro_mode(st.session_state.god_messages))
                print(response_data)
                # Display text response
                st.markdown(response_data['response'])
                
                # Handle visualization if present
                if response_data.get('graph_bool'):
                    fig, ax = plt.subplots(figsize=(10, 6))
                    
                    # Get data from response
                    x_labels = response_data.get('x_labels', [])
                    y_labels = response_data.get('y_labels', [])
                    x_values = response_data.get('x_values', [])
                    y_values = response_data.get('y_values', [])
                    
                    # Create line plot for each region
                    for i, region in enumerate(y_labels):
                        ax.plot(x_values, [y + i*50 for y in y_values], 
                               marker='o', label=region)
                    
                    # Customize plot
                    ax.set_xlabel(response_data.get('x_axis_name', 'Time'))
                    ax.set_ylabel(response_data.get('y_axis_name', 'Value'))
                    ax.set_title(response_data.get('title', 'Market Analysis'))
                    ax.grid(True)
                    ax.legend()
                    
                    # Display plot in Streamlit
                    st.pyplot(fig)
                    plt.close()
                
                # Add assistant response to chat history
                st.session_state.god_messages.append(
                    {"role": "assistant", "content": response_data['response']}
                )
