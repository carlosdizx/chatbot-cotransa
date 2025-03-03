import openai
import numpy as np
import pandas as pd
import os
from services.dynamodb_queries import get_regulation_prompt
from utils.env_config import load_config

# Cargar variables de entorno
OPENAI_API_KEY = load_config()["OPEN_AI_API_KEY"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

EMBEDDINGS_FILE = "normative_embeddings_cache.csv"  # Archivo donde guardaremos los embeddings


def get_embedding(text: str, model="text-embedding-ada-002") -> list:
    """Obtiene el embedding de un texto usando OpenAI Embeddings."""
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def cosine_similarity(vec1, vec2):
    """Calcula la similitud de coseno entre dos vectores."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def dividir_texto(texto, max_words=100):
    """Divide el texto en fragmentos más pequeños."""
    palabras = texto.split()
    return [" ".join(palabras[i:i + max_words]) for i in range(0, len(palabras), max_words)]


def embed_text():
    """Carga las normativas, las divide en fragmentos y obtiene embeddings."""
    normativas = get_regulation_prompt()
    fragmentos = []

    for normativa in normativas:
        fragmentos.extend(dividir_texto(normativa, max_words=100))  # Fragmentar en bloques de 100 palabras

    df = pd.DataFrame(fragmentos, columns=["text"])
    df["embedding"] = df["text"].apply(lambda x: get_embedding(x))  # Obtener embeddings
    df.to_csv(EMBEDDINGS_FILE, index=False)  # Guardar en CSV para no recalcular
    return df

def load_embeddings():
    """Carga los embeddings desde un archivo CSV."""
    if os.path.exists(EMBEDDINGS_FILE):
        df = pd.read_csv(EMBEDDINGS_FILE)
        df["embedding"] = df["embedding"].apply(lambda x: np.fromstring(x[1:-1], sep=" "))  # Convertir string a array
        return df
    else:
        return embed_text()  # Si no hay embeddings, generarlos

def find_relevant_regulation(query: str, n_resultados=3):
    """Busca los fragmentos de normativa más relevantes usando embeddings."""
    df = load_embeddings()  # Cargar normativas y embeddings
    query_embedding = get_embedding(query)  # Obtener embedding de la consulta

    df["similaridad"] = df["embedding"].apply(lambda x: cosine_similarity(x, query_embedding))
    df = df.sort_values(by="similaridad", ascending=False)

    fragmentos_relevantes = df.iloc[:n_resultados]["text"].tolist()  # Tomar los N fragmentos más relevantes
    return " ".join(fragmentos_relevantes)  # Unir los fragmentos relevantes
