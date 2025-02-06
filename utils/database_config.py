import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


def get_db_connection_string() -> str:

    db_server = os.environ.get("DB_SERVER")
    db_database = os.environ.get("DB_DATABASE")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")

    if not all([db_server, db_database, db_username, db_password]):
        raise EnvironmentError("No están definidas todas las variables de entorno para la base de datos.")

    connection_string = (
        f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
    return connection_string


def get_engine(echo: bool = False):
    connection_string = get_db_connection_string()
    engine = create_engine(connection_string, echo=echo)
    return engine


def get_session():
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()
