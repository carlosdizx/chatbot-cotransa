def process_file(file_text: str, chat_service) -> str:

    prompt = (
        "Analiza el siguiente contenido de un archivo y dame un resumen de la información "
        "relevante:\n\n" + file_text
    )
    messages = [{"role": "user", "content": prompt}]
    response = chat_service.generate_response(messages)
    return response
