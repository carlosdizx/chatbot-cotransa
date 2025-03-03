import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar cliente de DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
table = dynamodb.Table(TABLE_NAME)


def get_regulation_info() -> list:
    response = table.scan()

    results = []
    for item in response.get("Items", []):
        if "content" in item:
            results.append({
                "id": item.get("id"),
                "content": item["content"]
            })

    return results
