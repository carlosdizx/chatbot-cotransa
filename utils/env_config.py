import os
from dotenv import load_dotenv


def load_config() -> dict:
    load_dotenv()

    return {
        "OPEN_AI_API_KEY": os.getenv("OPEN_AI_API_KEY"),
        "MODEL": os.getenv("OPEN_AI_MODEL", 'gpt-4o-mini'),
        "TEMPERATURE": os.getenv("OPEN_AI_TEMPERATURE", 0),
        "CLOUDFRONT_URL_FILE": os.getenv("CLOUDFRONT_URL_FILE")
    }
