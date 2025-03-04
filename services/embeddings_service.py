import openai
import numpy as np
import pandas as pd
import requests
import io  # Importar io.StringIO para manejar texto en memoria
from utils.env_config import load_config

# Cargar configuración
config = load_config()
OPENAI_API_KEY = config["OPEN_AI_API_KEY"]
CLOUDFRONT_URL_FILE = config["CLOUDFRONT_URL_FILE"]  # URL directa del archivo en CloudFront

# Inicializar cliente OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str, model="text-embedding-ada-002") -> list:
    """Obtiene el embedding de un texto usando OpenAI Embeddings."""
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """Calcula la similitud de coseno entre dos vectores."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def download_embeddings():
    """Descarga el archivo de embeddings desde CloudFront y lo carga en un DataFrame."""
    try:
        response = requests.get(CLOUDFRONT_URL_FILE)
        response.raise_for_status()  # Lanza un error si la descarga falla

        # Convertir el CSV descargado directamente en DataFrame sin guardarlo en disco
        df = pd.read_csv(io.StringIO(response.text))

        print("📥 Embeddings descargados exitosamente desde CloudFront.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al descargar embeddings desde CloudFront: {e}")
        return None


def load_embeddings():
    """Carga los embeddings desde CloudFront."""
    df = download_embeddings()
    if df is None:
        print("⚠️ No se pudo descargar el archivo de embeddings. Es posible que no exista en S3.")
        return None

    # Convertimos la columna de embeddings de string a np.array
    df["embedding"] = df["embedding"].apply(lambda x: np.array([float(i) for i in x.split(",")]))

    # Filtrar embeddings inválidos
    df = df[df["embedding"].apply(lambda x: len(x) == 1536)]

    return df


def find_relevant_regulation(query: str, n_resultados=3):
    """Busca los fragmentos de normativa más relevantes usando embeddings."""
    df = load_embeddings()
    if df is None:
        return "⚠️ No se encontraron normativas relevantes debido a un error en la carga de embeddings."

    query_embedding = get_embedding(query)  # Obtener embedding de la consulta

    df["similaridad"] = df["embedding"].apply(lambda x: cosine_similarity(x, query_embedding))
    df = df.sort_values(by="similaridad", ascending=False)

    fragmentos_relevantes = df.iloc[:n_resultados]["text"].tolist()  # Obtener los N fragmentos más relevantes
    return " ".join(fragmentos_relevantes)