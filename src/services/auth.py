from datetime import UTC, datetime, timedelta

import jwt

from src.config import settings


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + timedelta(minutes=30),
        "iat": datetime.now(UTC),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return str(token)


def decode_access_token(token: str):
    try:
        decod_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decod_payload["sub"]

    except jwt.InvalidTokenError as e:
        print("Invalid token:", e)
        return None
