import os
from dotenv import load_dotenv


def load_config() -> dict:
    load_dotenv()

    required_env_vars = [
        "OPEN_AI_API_KEY", "CLOUDFRONT_URL_FILE", "DB_SERVER",
        "DB_DATABASE_1", "DB_DATABASE_2", "DB_USERNAME", "DB_PASSWORD"
    ]

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        error_message = f"ERROR: Faltan las siguientes variables de entorno: {', '.join(missing_vars)}"

        with open("missing_env_vars.txt", "w", encoding="utf-8") as file:
            file.write(error_message)

        raise EnvironmentError(error_message)
    return {
        "OPEN_AI_API_KEY": os.getenv("OPEN_AI_API_KEY"),
        "MODEL": os.getenv("OPEN_AI_MODEL", 'gpt-4o-mini'),
        "TEMPERATURE": os.getenv("OPEN_AI_TEMPERATURE", 0),
        "CLOUDFRONT_URL_FILE": os.getenv("CLOUDFRONT_URL_FILE"),
        "DB_SERVER": os.getenv("DB_SERVER"),
        "DB_DATABASE_1": os.getenv("DB_DATABASE_1"),
        "DB_DATABASE_2": os.getenv("DB_DATABASE_2"),
        "DB_USERNAME": os.getenv("DB_USERNAME"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "APP_IS_INTERN": os.getenv("APP_IS_INTERN") == "true",
    }
