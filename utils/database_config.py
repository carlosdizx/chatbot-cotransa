from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.env_config import load_config

config = load_config()


def get_db_connection_string(db_name: str) -> str:
    db_server = config["DB_SERVER"]
    db_username = config["DB_USERNAME"]
    db_password = config["DB_PASSWORD"]

    if db_name not in ["DB_DATABASE_1", "DB_DATABASE_2"]:
        raise ValueError(f"ERROR: Base de datos '{db_name}' no está definida en la configuración.")

    db_database = config[db_name]

    connection_string = (
        f"mssql+pymssql://{db_username}:{db_password}@{db_server}/{db_database}"
    )
    return connection_string


def get_engine(db_name: str, echo: bool = False):
    connection_string = get_db_connection_string(db_name)
    engine = create_engine(connection_string, echo=echo)
    return engine


def get_session(db_name: str):
    engine = get_engine(db_name)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()
