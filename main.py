import streamlit as st
from utils.env_config import load_config
from services.chat_service import ChatService
from utils.handle_user_query import handle_user_query
from interfaces.chat_service_interface import ChatServiceStrategy
from services.file_processing_service import process_file
from services.pdf_extractor_service import extract_text_from_pdf
import os
from utils.prompt import prompt_init, suggestion

config = load_config()

is_intern = config["APP_IS_INTERN"]
page_title = "Asistente Interno" if is_intern else "Asistente Contransa"
title_color = "#D35400" if is_intern else "#1F618D"


def init_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": prompt_init
            },
        ]


def display_messages() -> None:
    for message in st.session_state["messages"]:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    st.markdown(f"<h1 style='color:{title_color};'>{page_title}</h1>", unsafe_allow_html=True)

    chat_service: ChatServiceStrategy = ChatService(
        api_key=config["OPEN_AI_API_KEY"],
        model=config["MODEL"],
        temperature=config["TEMPERATURE"]
    )

    init_session_state()
    display_messages()
    st.info(suggestion)

    uploaded_file = st.file_uploader("Carga un archivo para procesar", type=["pdf"])
    if uploaded_file is not None:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        file_bytes = uploaded_file.read()

        if file_extension == ".pdf":
            file_text = extract_text_from_pdf(file_bytes)
        else:
            try:
                file_text = file_bytes.decode("utf-8")
            except Exception:
                file_text = file_bytes.decode("latin-1")

        if st.button("Procesar archivo"):
            try:
                file_response = handle_user_query(process_file(file_text, chat_service))
                st.session_state["messages"].append({"role": "assistant", "content": file_response})
                with st.chat_message("assistant"):
                    st.markdown(file_response)
            except Exception as e:
                st.error(f"Error al procesar el archivo: {e}")

    prompt = st.chat_input("Escribe tu mensaje...")

    if prompt:
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.status("Procesando tu consulta...", expanded=True) as status:
                provider_response = chat_service.generate_response(st.session_state["messages"])
                response = handle_user_query(provider_response)
                status.update(label="¡Respuesta generada!", state="complete", expanded=False)
        except Exception as e:
            st.error(str(e))
            print(e)
            response = "Lo siento, ocurrió un error al procesar tu solicitud."

        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


if __name__ == "__main__":
    main()
