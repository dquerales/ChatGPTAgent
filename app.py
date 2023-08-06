import streamlit as st
import pandas as pd
import json

from agent import query_agent, create_agent

def decode_response(response: str) -> dict:
    #This function converts the string response from the model to a dictionary object.
    return json.loads(response)


def write_response(response_dict: dict):
    #Write a response from an agent to a Streamlit app.

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

st.set_page_config(page_title="CHATGPT Agent App", page_icon="🤖")

with st.sidebar:
    st.header('ChatGPT Agent')
    st.markdown('Chat GPT Agent using Langchain tools')
    st.markdown('Made by [Daniel Querales](mailto:d.querales@gmail.com)')

st.title("🤖 ChatGPT Agent LLM for Data Exploration")

st.header('Upload your dataset')
df = st.file_uploader("Upload your CSV")

st.header('Chat')
API_KEY = st.text_input("Insert your secret API_KEY")

query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file.
    agent = create_agent(df, API_KEY)

    # Query the agent.
    response = query_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_response(decoded_response)
