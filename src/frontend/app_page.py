import os
import sys

# Ensure the current directory is added to the path for imports
CUR_DIR = os.getcwd().replace("\\", "/").replace('/exp', '')
sys.path.append(CUR_DIR)

import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from src.app.schemas.llm import ChatRequest, Message
from src.app.llm import LiteLLMKit
from src.analysis.market_analysis import get_market_report
from src.analysis.customer_discoverer import get_customer_discoverer
import asyncio

# Load environment variables
load_dotenv()



# Title of the app
st.title("AI Market Edge Assistant")

# Initialize the LLM client
client = LiteLLMKit(model_name="gemini-1.5-flash", temperature=0.7, max_tokens=1024, stream=False)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.awaiting_input = False  # Track whether we're waiting for user input

# Steps for the flow
async def analysis_step(analysis_topic: str):
    # Asynchronous calls to fetch data
    customer_analysis = await get_customer_discoverer(analysis_topic)
    report, graph = await get_market_report(analysis_topic)
    combined_analysis = (
        f"**Customer Insights:** {customer_analysis}\n\n"
        f"**Market Analysis Report:** {report}"
    )
    return combined_analysis, graph

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "graph" in message:  # Check if there's a graph to display
            st.image(message["graph"], caption="Market Analysis Graph")

# Check if we need to send the initial question
if not st.session_state.awaiting_input:
    initial_question = "Which market would you like to analyze?"
    st.session_state.messages.append({"role": "assistant", "content": initial_question})
    with st.chat_message("assistant"):
        st.markdown(initial_question)
    st.session_state.awaiting_input = True

# Accept user input
if prompt := st.chat_input("Your response here..."):
    try:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.awaiting_input = False  # Reset the input flag
        
        # Display user message in chat
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Display asistant message in chat
        st.session_state.messages.append({"role": "assistant", "content": "Please wait while we analyse the market for you!This may take upto 10 mins"})
        with st.chat_message("assistant"):
            st.markdown("Please wait while we analyse the market for you!")

        # Proceed to analysis
        response_text, graph = asyncio.run(analysis_step(prompt))  # Perform analysis
        with st.chat_message("assistant"):
            st.markdown(response_text)
            if graph:
                st.image(graph, caption="Market Analysis Graph")
        st.session_state.messages.append({"role": "assistant", "content": response_text, "graph": graph})
    except Exception as e:
        # Restart conversation on error
        st.error("An error occurred. Restarting conversation.")
        st.session_state.messages.clear()
