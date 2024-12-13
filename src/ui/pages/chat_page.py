import streamlit as st
from database import save_report, get_user_reports
from api_code import chat
import json

def show_chat_page():
    st.header("Chat with Market Analysis AI")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know about market analysis?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = json.loads(chat(st.session_state.messages))['response']
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
