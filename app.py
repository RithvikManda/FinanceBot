import os
import json
import pandas as pd
import streamlit as st
from groq import Groq


df1=pd.read_csv("C:/Users/HP/OneDrive/Desktop/finance/datasets/AAPL_monthly_data.csv") #path to dataset1
df2=pd.read_csv("C:/Users/HP/OneDrive/Desktop/finance/datasets/AMZN_monthly_data.csv") #path to dataset2
df3=pd.read_csv("C:/Users/HP/OneDrive/Desktop/finance/datasets/AVGO_monthly_data.csv") #path to dataset3
df4=pd.read_csv("C:/Users/HP/OneDrive/Desktop/finance/datasets/META_monthly_data.csv") #path to dataset4
df5=pd.read_csv("C:/Users/HP/OneDrive/Desktop/finance/datasets/MSFT_monthly_data.csv") #path to dataset5

df1_sample = df1.to_string(index=False)
df2_sample = df2.to_string(index=False)
df3_sample = df3.to_string(index=False)
df4_sample = df4.to_string(index=False)
df5_sample = df5.to_string(index=False)
# df=df1_sample+df2_sample+df3_sample+df4_sample+df5_sample

df = f"{df1_sample}\n\n{df2_sample}\n\n{df3_sample}\n\n{df4_sample}\n\n{df5_sample}"

# print(df)

st.set_page_config(
    page_title="Finance Chat",
    page_icon="🦙",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# save the api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# streamlit page title
st.title("🦙 Finance ChatBot")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sens user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": f"""
            You are a highly skilled Finance Assistant AI specializing in stock performance measurement and risk analytics. Your primary tasks include fetching historical stock and benchmark data using APIs like Yahoo Finance, calculating monthly, cumulative, and annualized returns over various periods (1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y), and computing risk statistics like Sharpe Ratios to identify the best-performing stock by return per unit risk. You generate clear, actionable insights, create visualizations (e.g., rebased stock price charts), and guide users in building technical solutions, such as integrating APIs into web interfaces for data retrieval. Always provide precise, concise, and user-friendly explanations for calculations, insights, or code implementations, and proactively ask clarifying questions when user inputs are incomplete.
            {df}
            Calculate monthly, cumulative, and annualized returns over various periods (1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y), and computing risk statistics like Sharpe Ratios to identify the best-performing stock by return per unit risk based on this data. Please provide the results.  Don't show me the code that you have used this is a strict warning only show the results for the user input. When you display the output display it properly with propoer identation.   """},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)