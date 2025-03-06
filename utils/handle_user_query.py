import json
from services.db_queries import get_envio_status, search_company
from services.embeddings_service import find_relevant_regulation
from services.chat_service import ChatService  # Para llamar a la IA
from utils.env_config import load_config
from utils.prompt import prompt_aux  # Importamos el prompt auxiliar

# Configuración de la IA
config = load_config()
chat_service = ChatService(
    api_key=config["OPEN_AI_API_KEY"],
    model=config["MODEL"],
    temperature=config["TEMPERATURE"]
)


def format_regulation_response(normativa: str) -> str:
    """Usa la IA para formatear la respuesta de la normativa."""
    messages = [
        {"role": "system", "content": prompt_aux},
        {"role": "user", "content": normativa}
    ]

    try:
        formatted_response = chat_service.generate_response(messages)
        return formatted_response
    except Exception as e:
        return f"Error al formatear la respuesta: {str(e)}"


def handle_user_query(user_query: str):
    """Procesa la consulta del usuario."""
    try:
        jsonData = json.loads(user_query)
    except Exception as e:
        print(user_query)
        print(f"Error al procesar JSON {str(e)}")
        return f"Algo ha ido mal, danos un momento mientras lo resolvemos"

    try:
        if jsonData["action"] == "get_envio_status":
            return get_envio_status(jsonData["response"])

        elif jsonData["action"] == "get_regulation_info":
            normativa_relevante = find_relevant_regulation(jsonData["query"])
            respuesta_formateada = format_regulation_response(normativa_relevante)
            return f"📜 **Normativa Relevante:**\n\n{respuesta_formateada}"

        elif jsonData["action"] == "request_file":
            return jsonData["response"]

        elif jsonData["action"] == "natural_response":
            return jsonData["response"]

        elif jsonData["action"] == "search_company":
            return search_company(jsonData["query"])

        else:
            return "No entendí tu solicitud. ¿Puedes reformularla?"

    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"
