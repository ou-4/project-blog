import uuid

import boto3
from botocore.client import Config

from src.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
    aws_access_key_id=settings.MINIO_ROOT_USER,
    aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
    config=Config(signature_version="s3v4"),
)


def upload_file(file: bytes, filename: str):
    extension = filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{extension}"

    s3_client.put_object(Bucket=settings.MINIO_BUCKET, Key=unique_name, Body=file)

    url = f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{unique_name}"

    return url
