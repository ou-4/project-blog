from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import engine, get_db
from src.middleware import check_auth
from src.routing.article import router_article
from src.routing.auth import router_auth
from src.routing.category import router_category
from src.services.s3 import ensure_bucket


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect():
            print("Connected successfully")
        ensure_bucket()
        print("MinIO bucket ready")
    except Exception as e:
        print(f"Database connection error: {e}")

    yield

    await engine.dispose()


CORS_ORIGINS = ["http://localhost:3000"]

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_credentials=True, allow_origins=CORS_ORIGINS)
app.middleware("http")(check_auth)
app.include_router(router_auth)
app.include_router(router_category)
app.include_router(router_article)


@app.get("/health")
async def health(session: AsyncSession = Depends(get_db)):
    try:
        _ = await session.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="База данных не работает") from None
