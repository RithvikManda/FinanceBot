import os
import json
import pandas as pd
import streamlit as st
from groq import Groq


# df1=pd.read_csv("dataset/amazon_inv.csv") #path to dataset1
# df2=pd.read_csv("dataset/apple_inv.csv") #path to dataset2
# df3=pd.read_csv("dataset/meta_inv.csv") #path to dataset3
# df4=pd.read_csv("dataset/ndx_inv.csv") #path to dataset4
# df5=pd.read_csv("dataset/nvidia_inv.csv") #path to dataset5

# df1_sample = df1.to_string(index=False)
# df2_sample = df2.to_string(index=False)
# df3_sample = df3.to_string(index=False)
# df4_sample = df4.to_string(index=False)
# df5_sample = df5.to_string(index=False)
# # df=df1_sample+df2_sample+df3_sample+df4_sample+df5_sample

# df = f"{df1_sample}\n\n{df2_sample}\n\n{df3_sample}\n\n{df4_sample}\n\n{df5_sample}"

# print(df)

st.set_page_config(
    page_title="Blog Generater",
    page_icon="🦙",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


st.title("Blogify AI")

# url = "https://discuss.streamlit.io/t/streamlit-hyperlink/29831"
# st.write("Check of visualizations(%s)" % url)


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": """
        You are a skilled blog writer and SEO expert. Your task is to create a blog title and a detailed blog based on the given input. 

        Input: {user_input}

        1. Generate an engaging, SEO-friendly title for the blog. Ensure it is concise and appealing to the target audience. 
        2. Write a comprehensive blog based on the input, including:
            - An attention-grabbing introduction that sets the context.
            - Well-structured body content divided into clear subheadings.
            - A conclusion summarizing the key points and providing a call-to-action if applicable.
        3. Ensure the tone is professional and informative. Aim for readability and value to the reader.

        Begin by providing the title, followed by the blog content.
        """
            },
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