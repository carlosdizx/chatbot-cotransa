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


def search_company(query: str):
    print(query)
    print("Entre")
    session = get_session()
    try:
        sql_query = text("""
            SELECT TOP (1000) 
                Nombre_Empresa, 
                CIF_NIF, 
                EORI, 
                Empresa AS Propietario, 
                FechaBloqueo, 
                MotivoBloqueo, 
                ient_cli,
                CASE 
                    WHEN Nombre_Empresa LIKE :exact_match THEN 1.0
                    WHEN Nombre_Empresa LIKE :partial_match THEN 0.8
                    ELSE 0.0
                END AS Match_Probability
            FROM BotCotransaAI.dbo.EmpresasGrupo
            WHERE 
                CIF_NIF = :query 
                OR Nombre_Empresa LIKE :partial_match
            ORDER BY Match_Probability DESC, Nombre_Empresa;
        """)
        print(f"sql query {sql_query}")

        results = session.execute(sql_query, {
            "query": query,
            "exact_match": query + '%',
            "partial_match": '%' + query + '%'
        }).fetchall()

        print("results", results)

        if results:
            response = "### Empresas encontradas:\n\n"
            response += "| Empresa | CIF/NIF | EORI | Estado |\n"
            response += "|---------|---------|------|--------|\n"

            for company in results:
                estado = "🚫 **Bloqueada**" if company.FechaBloqueo else "✅ **Activa**"
                response += f"| **{company.Nombre_Empresa}** | {company.CIF_NIF} | {company.EORI or 'N/A'} | {estado} |\n"

            response += "\n\n📌 *Si necesitas más detalles de alguna empresa, proporciona el CIF/NIF específico.*"
            return response
        else:
            return "⚠️ No encontré empresas con esa búsqueda. Intenta con otro nombre o CIF/NIF."

    except Exception as e:
        print(e)
        return f"❌ Error al consultar la base de datos: {e}"

    finally:
        session.close()
