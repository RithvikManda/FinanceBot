import os
import json
import pandas as pd
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Blog Generator",
    page_icon="🦙",
    layout="wide"  # Set layout to wide for better alignment
)

# Load configuration and set API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Add custom CSS for sticky input and scrollable chat container
st.markdown(
    """
    <style>
    .chat-container {
        max-height: calc(100vh - 150px); /* Adjust to fit the viewport */
        overflow-y: auto; /* Enable scrolling */
        padding: 10px;
        margin-bottom: 80px; /* Space for the footer */
    }
    .fixed-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        box-shadow: 0px -4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .chat-message {
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Chat history display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Fixed footer for input
st.markdown('<div class="fixed-footer">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 8])

with col1:
    st.title("Blogify AI", anchor=False)

with col2:
    user_prompt = st.chat_input("Ask LLAMA...")
    word_limit = st.selectbox(
        "Word Limit",
        options=[50, 100, 200, 300, 500],
        index=1,
        label_visibility="collapsed"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Build messages for the API request
    messages = [
        {"role": "system", "content": f"""
            Give me an entire blog on the topic '{user_prompt}' with approximately {word_limit} words and considering the role as '{role}'.        """},
        *st.session_state.chat_history
    ]

    # Make API call
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    # Extract response and display it
    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
