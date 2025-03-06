from sqlalchemy import text
from utils.database_config import get_session


def get_envio_status(tracking_number: str):
    session = get_session()
    try:
        query = text(f"SELECT * FROM EnviosActivos WHERE Ref_Partida = :tracking_number;")
        result = session.execute(query, {"tracking_number": tracking_number}).fetchone()
        if result:
            return (f"El estado de tu envío es: {result.Descripcion_Hito}.\n\n"
                    f" Origen: {result.Puerto_Origen}, {result.Pais_Origen}.\n\n"
                    f" Destino: {result.Puerto_Destino}, {result.Pais_Destino}.\n\n"
                    f" Peso (KG): {result.Kg_Brutos}")
        else:
            return "No encontré información para ese número de seguimiento."
    except Exception as e:
        print(e)
        return f"Error al consultar la base de datos: {e}"
    finally:
        session.close()
