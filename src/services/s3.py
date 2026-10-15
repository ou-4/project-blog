import json
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


def ensure_bucket():
    try:
        s3_client.head_bucket(Bucket=settings.MINIO_BUCKET)
    except Exception:
        s3_client.create_bucket(Bucket=settings.MINIO_BUCKET)


def upload_file(file, filename: str):
    extension = filename.split(".")[-1]
    unique_name = f"{uuid.uuid4()}.{extension}"
    s3_client.upload_fileobj(file, settings.MINIO_BUCKET, unique_name)
    return unique_name


def build_public_url(unique_name):
    return f"{settings.MINIO_PUBLIC_URL}/{settings.MINIO_BUCKET}/{unique_name}"


def object_exists(key):
    try:
        s3_client.head_object(Bucket=settings.MINIO_BUCKET, Key=key)
        return True
    except Exception:
        return False


def set_bucket_public_policy():
    policy_dict = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET}/*"],
            }
        ],
    }

    s3_client.put_bucket_policy(Bucket=settings.MINIO_BUCKET, Policy=json.dumps(policy_dict))
