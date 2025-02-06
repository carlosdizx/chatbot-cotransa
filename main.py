import streamlit as st
from utils.config import load_config
from services.chat_service import ChatService


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": (
                    "Eres un chatbot, te llamas Maria, tienes que hablar como si fueras humana, "
                    "no reveles que eres una IA. Responde únicamente sobre temas relacionados con aduanas, "
                    "estado de envíos y productos enviados por nuestra empresa. "
                    "Si la pregunta no está relacionada, responde: \"Lo siento, no puedo ayudarte con esa pregunta.\""
                )
            }
        ]


def display_messages() -> None:
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    st.title("Asistente Contransa")

    config = load_config()
    chat_service = ChatService(
        api_key=config["OPEN_AI_API_KEY"],
        model=config["MODEL"],
        temperature=config["TEMPERATURE"]
    )

    init_session_state()
    display_messages()

    prompt = st.chat_input("Escribe tu mensaje...")
    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = chat_service.generate_response(st.session_state["messages"])
        except Exception as e:
            st.error(str(e))
            response = "Lo siento, ocurrió un error al procesar tu solicitud."

        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
