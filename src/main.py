from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.session import engine
from src.middleware import check_auth
from src.routing.article import router_article
from src.routing.auth import router_auth
from src.routing.category import router_category


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect():
            print("Connected successfully")
    except Exception as e:
        print(f"Database connection error: {e}")

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.middleware("http")(check_auth)
app.include_router(router_auth)
app.include_router(router_category)
app.include_router(router_article)


@app.get("/health")
async def health():
    return {"status": "ok"}
