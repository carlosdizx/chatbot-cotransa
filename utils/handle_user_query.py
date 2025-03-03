import json
from services.db_queries import get_envio_status
from services.embeddings_service import find_relevant_regulation  # Ahora usamos esta función


def handle_user_query(user_query: str):
    """Procesa la consulta del usuario."""
    try:
        jsonData = json.loads(user_query)
    except Exception as e:
        print(user_query)
        print(f"Error al procesar json {str(e)}")
        return f"Algo ha ido mal, danos un momento mientras lo resolvemos"
    try:

        if jsonData["action"] == "get_envio_status":
            return get_envio_status(jsonData["response"])

        elif jsonData["action"] == "get_regulation_info":
            normativa_relevante = find_relevant_regulation(jsonData["query"])
            return f"Basado en nuestras normativas, la respuesta es:\n\n{normativa_relevante}"

        elif jsonData["action"] == "request_file":
            return jsonData["response"]

        elif jsonData["action"] == "natural_response":
            return jsonData["response"]

        else:
            return "No entendí tu solicitud. ¿Puedes reformularla?"

    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"
