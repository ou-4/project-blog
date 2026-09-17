from fastapi import Request
from fastapi.responses import JSONResponse

from src.services.auth import decode_access_token

PUBLIC_PATHS = [
    "/auth/register",
    "/auth/login",
    "/health",
    "/docs",
    "/openapi.json",
    "/categories",
    "/articles",
]


async def check_auth(request: Request, call_next):
    if any(request.url.path.startswith(prefix) for prefix in PUBLIC_PATHS):
        return await call_next(request)

    token = request.cookies.get("access_token")

    if not token:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    user_id = decode_access_token(token)

    if user_id is None:
        return JSONResponse(status_code=401, content={"detail": "Invalid token"})

    return await call_next(request)
