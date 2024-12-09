import os
import json
import pandas as pd
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Blog Generater",
    page_icon="🦙",
    layout="centered"
)

# Add custom CSS for sticky dropdowns
st.markdown(
    """
    <style>
    .sticky-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        background-color: white;
        padding: 10px 0;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .content-container {
        margin-top: 120px; /* Space for the sticky container */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load configuration
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sticky container for dropdowns
st.markdown('<div class="sticky-container">', unsafe_allow_html=True)
st.title("Blogify AI")
# with st.container():
#     col1, col2, col3 = st.columns([5, 2, 2])

#     with col3:
        
#     with col2:
        
st.markdown('</div>', unsafe_allow_html=True)

# Content container for chat history and input
st.markdown('<div class="content-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask LLAMA...")
word_limit = st.selectbox(
            "Word Limit",
            options=[50, 100, 200, 300, 500],
            index=1,
            label_visibility="collapsed"
        )

role = st.selectbox(
            "Role",
            options=['Researcher', 'Student', 'Teacher', 'Analyst'],
            index=1,
            label_visibility="collapsed"
        )

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": f"""
        Give me an entire blog on the topic '{user_prompt}' with approximately {word_limit} words and considering the role as '{role}'.
        """},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
st.markdown('</div>', unsafe_allow_html=True)
