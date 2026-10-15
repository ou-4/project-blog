from unittest.mock import AsyncMock, patch

from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import test_settings
from src.db.base import Base
from src.db.session import get_db
from src.main import app
from src.project_blog.models import ArticleChunk

test_engine = create_async_engine(test_settings.TEST_DATABASE_URL, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture(autouse=True)
def mock_celery():
    with patch("src.services.user.send_welcome_email.delay") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_embed():
    with patch("src.services.ai.embed", new=AsyncMock(return_value=[0.0] * 768)) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_generate():
    with patch("src.services.ai.generate", new=AsyncMock(return_value="Test answer")) as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_upload():
    with patch("src.services.article.upload_file") as mock:
        mock.return_value = "test_key.png"
        yield mock


@pytest.fixture(autouse=True)
def mock_object():
    with patch("src.services.article.object_exists") as mock:
        mock.return_value = True
        yield mock


@pytest.fixture(autouse=True)
def mock_index():
    with patch("src.services.article.index_article.delay") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_search_similar_chunks():
    with patch(
        "src.services.ai.search_similar_chunks",
        new=AsyncMock(return_value=[ArticleChunk(article_id=1, content="Test content")]),
    ) as mock:
        yield mock


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client):
    _ = await client.post(
        "/auth/register", json={"email": "etest@bk.ru", "password": "qwerty12345"}
    )
    response2 = await client.post(
        "/auth/login", json={"email": "etest@bk.ru", "password": "qwerty12345"}
    )
    assert response2.status_code == 200
    return client
