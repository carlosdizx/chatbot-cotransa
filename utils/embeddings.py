import openai
import numpy as np
import pandas as pd
import os
from services.dynamodb_queries import get_regulation_prompt
from utils.env_config import load_config

# Cargar variables de entorno
OPENAI_API_KEY = load_config()["OPEN_AI_API_KEY"]

# Configurar clave de API
openai.api_key = OPENAI_API_KEY

EMBEDDINGS_FILE = "embeddings_cache.csv"  # Archivo donde almacenaremos los embeddings


def get_embedding(text: str, model="text-embedding-ada-002") -> list:
    """Obtiene el embedding de un texto usando OpenAI Embeddings."""
    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response["data"][0]["embedding"]


def cosine_similarity(vec1, vec2):
    """Calcula la similitud de coseno entre dos vectores."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def load_embeddings():
    """Carga los embeddings desde un archivo CSV si existe, o los genera y los guarda."""
    if os.path.exists(EMBEDDINGS_FILE):
        df = pd.read_csv(EMBEDDINGS_FILE)
        df["embedding"] = df["embedding"].apply(lambda x: np.fromstring(x[1:-1], sep=" "))  # Convertir string a array
    else:
        normativas = get_regulation_prompt()  # Obtener normativas desde DynamoDB
        df = pd.DataFrame(normativas, columns=["text"])
        df["embedding"] = df["text"].apply(lambda x: get_embedding(x))  # Generar embeddings
        df.to_csv(EMBEDDINGS_FILE, index=False)  # Guardar embeddings para evitar recalcularlos
    return df


def find_relevant_regulation(query: str):
    """Busca la normativa más relevante usando embeddings."""
    df = load_embeddings()  # Cargar normativas y embeddings
    query_embedding = get_embedding(query)  # Obtener embedding de la consulta
    df["similaridad"] = df["embedding"].apply(lambda x: cosine_similarity(x, query_embedding))
    df = df.sort_values(by="similaridad", ascending=False)

    return df.iloc[0]["text"] if not df.empty else "No encontré información relevante."

