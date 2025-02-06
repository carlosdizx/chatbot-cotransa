import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI

load_dotenv()

try:
    openai_api_key = os.environ["OPEN_AI_API_KEY"]
except KeyError:
    raise EnvironmentError("La variable de entorno OPEN_AI_API_KEY no está definida.")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=openai_api_key)

st.title("Asistente Contransa")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": """
            Eres un chatbot, te llamas Maria, tienes que hablar 
            como si fueras humana, no reveles que eres una IA,
            Responde únicamente sobre temas relacionados con aduanas,
            estado de envíos y productos enviados por nuestra empresa.
            Si la pregunta no está relacionada, responde: "Lo siento, no puedo ayudarte con esa pregunta."
            """
        }
    ]

for message in st.session_state["messages"]:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escribe tu mensaje...")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = llm.invoke(st.session_state["messages"]).content
    except Exception as e:
        st.error(f"Error al generar la respuesta: {e}")
        response = "Lo siento, ocurrió un error al procesar tu solicitud."

    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
