from sqlalchemy import text
from utils.database_config import get_session


def get_envio_status(tracking_number: str):
    session = get_session()
    try:
        query = text("SELECT * FROM EnviosActivos "
                     "WHERE Ref_Partida = :tracking_number OR Ref_Expediente = :tracking_number;")
        result = session.execute(query, {"tracking_number": tracking_number}).fetchone()
        if result:
            return f"El estado de tu envío es: {result.status}. Última actualización: {result.last_update}. Destino: {result.destination}."
        else:
            return "No encontré información para ese número de seguimiento."
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"
    finally:
        session.close()
