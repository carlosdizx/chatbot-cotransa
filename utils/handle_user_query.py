import json
from services.db_queries import get_envio_status


def handle_user_query(user_query: str):

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
            return f"Consultando regulaciones: {jsonData['query']} en la base de datos de DynamoDB."

        elif jsonData["action"] == "request_file":
            return jsonData["response"]

        elif jsonData["action"] == "natural_response":
            return jsonData["response"]

        else:
            return "No entendí tu solicitud. ¿Puedes reformularla?"

    except Exception as e:
        return f"Error al procesar la consulta: {str(e)}"
