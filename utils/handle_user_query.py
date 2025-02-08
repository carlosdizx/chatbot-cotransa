import json

from services.db_queries import get_envio_status


def handle_user_query(user_query: str):
    jsonData = json.loads(user_query)

    if jsonData['action'] == 'get_envio_status':
        return get_envio_status(jsonData['response'])
    elif jsonData['action'] == 'natural_response':
        return jsonData['response']
    else:
        raise NotImplementedError("Lo siento, algo ha ido mal.")
