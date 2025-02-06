import os
from dotenv import load_dotenv


def load_config() -> dict:
    load_dotenv()
    try:
        openai_api_key = os.environ["OPEN_AI_API_KEY"]
    except KeyError:
        raise EnvironmentError("La variable de entorno OPEN_AI_API_KEY no está definida.")

    return {
        "OPEN_AI_API_KEY": openai_api_key,
        "MODEL": "gpt-4o-mini",
        "TEMPERATURE": 0,
    }
