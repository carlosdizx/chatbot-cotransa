import streamlit as st
from utils.env_config import load_config
from services.chat_service import ChatService
from utils.handle_user_query import handle_user_query
from interfaces.chat_service_interface import ChatServiceStrategy


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": (
                    "Eres un chatbot, te llamas MarIA, tienes que hablar como si fueras humana"
                    "Responde únicamente sobre temas relacionados con aduanas, estado de envíos y productos enviados "
                    "por nuestra"
                    "empresa."
                    "Analiza la consultas del usuario y determina si se requiere realizar una consulta "
                    "a la base de datos. "
                    "Si es así, responde únicamente en formato JSON indicando la acción y los parámetros necesarios. "
                    "Por ejemplo,"
                    "si se requiere consultar el estado de un envío, responde exactamente de esta forma: \n\n"
                    '{"action": "get_envio_status", "response": "<número>"}\n\n'
                    "Si no es necesaria una consulta a la base de datos, responde únicamente con un mensaje natural "
                    "para el de la siguiente forma en formato JSON:\n\n"
                    '{"action": "natural_response", "response": "<response>"}\n\n'
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

    chat_service: ChatServiceStrategy = ChatService(
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
            provider_response = chat_service.generate_response(st.session_state["messages"])
            response = handle_user_query(provider_response)
        except Exception as e:
            st.error(str(e))
            response = "Lo siento, ocurrió un error al procesar tu solicitud."

        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
