def process_file(file_text: str, chat_service) -> str:
    prompt = (
            "Analiza el siguiente contenido de un archivo y determina si contiene un número de seguimiento "
            "para un pedido. Si lo contiene, responde en formato JSON exactamente de la siguiente forma:\n\n"
            '{"action": "get_envio_status", "response": "<tracking_number>"}\n\n'
            "Si no se encuentra un número de seguimiento, responde en formato JSON de la siguiente forma:\n\n"
            '{"action": "natural_response", "response": "<mensaje>"}\n\n'
            "Contenido del archivo:\n\n" + file_text
    )
    messages = [{"role": "user", "content": prompt}]
    response = chat_service.generate_response(messages)
    return response
