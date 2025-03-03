import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar cliente de DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
table = dynamodb.Table(TABLE_NAME)


def get_regulation_prompt() -> list:
    response = table.scan()

    results = []
    for item in response.get("Items", []):
        if "content" in item:
            results.append(item["content"])

    return results
