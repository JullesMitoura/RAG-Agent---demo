import streamlit as st
from app.agent import CustomAgent
from app.services.qdrant_service import QdrantService

def chat(selected_collection):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm the chatbot and I can help you with queries regarding information about processes and documents. How can I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking ... "):
                response = CustomAgent().agent_exec(prompt, selected_collection)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)