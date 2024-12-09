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


# # Create a fixed header container
# st.markdown('<div class="header-container">', unsafe_allow_html=True)
st.title("Blogify AI")
with st.container():
    col1, col2,col3 = st.columns([5, 2,2])

    with col3:
        word_limit = st.selectbox(
            "Word Limit",
            options=[50, 100, 200, 300, 500],
            index=1,
            label_visibility="collapsed"
        )
    # Replace the single select dropdown with multiselect
    with col2:
        role = st.selectbox(
            "Word Limit",
            options=['Researcher', 'Student', 'Teacher', 'Analyst'],
            index=1,
            label_visibility="collapsed"
        
    )


    with col1:
        user_prompt = st.chat_input("Ask LLAMA...")

# st.markdown('</div>', unsafe_allow_html=True)

# Chat history display with a scrollable container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Build messages for the API request
    messages = [
        {"role": "system", "content": f"""
        Give me an entire blog on the topic '{user_prompt}' with approximately {word_limit} words try to make it very concise according to the {role} role and which can be understood by {role}.
        """},
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
    # print(role)
