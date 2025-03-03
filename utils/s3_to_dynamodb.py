import boto3
import json
import datetime
import os
import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración desde .env
TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
PDF_LIST_FILE = os.getenv("PDF_LIST_FILE", "pdf_urls.txt")

# Configurar cliente de AWS
dynamodb = boto3.resource("dynamodb", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION)

table = dynamodb.Table(TABLE_NAME)


def read_pdf_from_url(url):
    """Descarga y extrae el contenido de un PDF desde una URL pública."""
    response = requests.get(url)
    response.raise_for_status()

    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    pdf_reader = PdfReader("temp.pdf")
    text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text.strip() if text else "No se pudo extraer el texto."


def save_to_dynamodb(file_name, content):
    """Guarda el archivo en DynamoDB."""
    now = datetime.datetime.now(datetime.UTC).isoformat()
    table.put_item(
        Item={
            "id": file_name,  # Usar file_name como clave primaria 'id'
            "original_file_name": file_name,
            "content": content,
            "created_at": now,
            "updated_at": now,
            "is_active": True
        }
    )
    print(f"Documento {file_name} guardado en DynamoDB")


def process_documents():
    """Lee el archivo con URLs de PDFs y procesa cada uno."""
    if not os.path.exists(PDF_LIST_FILE):
        print(f"El archivo {PDF_LIST_FILE} no existe.")
        return

    with open(PDF_LIST_FILE, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    for url in urls:
        file_name = url.split("/")[-1]  # Extraer el nombre del archivo desde la URL
        print(f"Procesando: {file_name}")
        content = read_pdf_from_url(url)
        save_to_dynamodb(file_name, content)

    print("Todos los documentos han sido procesados.")


if __name__ == "__main__":
    process_documents()
