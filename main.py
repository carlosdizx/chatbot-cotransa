import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI

load_dotenv()
openai_api_key = None

try:
    openai_api_key = os.environ["OPEN_AI_API_KEY"]
except KeyError:
    raise EnvironmentError("La variable de entorno OPEN_AI_API_KEY no está definida.")

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=openai_api_key)

st.title("Asistente Contransa")

messages = [
    ("system", """
    Eres un chatbot, te llamas Maria, tienes que hablar 
    como si fueras humana, no reveles que eres una IA
    """)]

if messages not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.append(["human", prompt])

    response = llm.invoke(messages).content
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"content": response, "role": "assistant"})
