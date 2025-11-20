import streamlit as st
from interface import Interface
from pathlib import Path
from dotenv import load_dotenv
from load_policies import load_policies
from typing import List

load_dotenv()

st.header("HR helper PoC")

@st.cache_resource
def _load_policies(policy_path: str):
    return load_policies(policy_path)

@st.cache_resource
def load_and_add_policies(policies: List[str]):
    chatbot = Interface("hr_policies")
    for name, text in policies.items():
        chatbot.add_policy(name, text)
    return chatbot

def fake_streaming_response(response: str):
    import time
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

policies = _load_policies("./Policies")
chatbot = load_and_add_policies(policies)

for name, text in policies.items():
    with st.expander(f"Policy: {name}"):
        st.write(text)

prompt = st.chat_input("Ask")
if prompt:
    chatbot_response = chatbot.ask(prompt)
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write_stream(fake_streaming_response(chatbot_response))
