from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from src.repositories.article import (
    create_article_repo,
    delete_article_repo,
    get_article_by_id_repo,
    get_articles_repo,
    update_article_repo,
)
from src.repositories.category import get_category_by_id
from src.schemas.article import ArticleListResponse
from src.services.s3 import build_public_url, object_exists, upload_file
from src.worker import index_article

ALLOWED_TYPES = ["image/jpeg", "image/png"]
MAX_SIZE = 5 * 1024 * 1024


async def create_article(
    session: AsyncSession, title: str, content: str, category_id: int, image_key: str
):
    if await get_category_by_id(session, category_id) is None:
        raise HTTPException(status_code=404, detail="Категории такой нет")

    if not object_exists(image_key):
        raise HTTPException(status_code=400, detail="Такого ключа нет")

    url = build_public_url(image_key)

    article = await create_article_repo(session, title, content, category_id, url)
    await session.commit()
    index_article.delay(article.id)
    return article


async def get_articles(
    session: AsyncSession,
    page_number: int,
    page_size: int,
    category_id: int | None = None,
    search: str | None = None,
):
    articles, total = await get_articles_repo(session, page_number, page_size, category_id, search)
    return ArticleListResponse(
        items=articles,
        total=total,
        page_number=page_number,
        page_size=page_size,
    )


async def get_article_by_id(session: AsyncSession, article_id: int):
    article = await get_article_by_id_repo(session, article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="Такого article нет")

    if article.is_deleted:
        raise HTTPException(status_code=404, detail="Article удален")

    return article


async def update_article(session, article_id, title, content, category_id, image_url):
    article = await get_article_by_id_repo(session, article_id)

    if article is None or article.is_deleted:
        raise HTTPException(status_code=404, detail="Article not found")

    if category_id is not None:
        category = await get_category_by_id(session, category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    updated = await update_article_repo(session, article_id, title, content, category_id, image_url)
    await session.commit()
    index_article.delay(article.id)
    await session.refresh(updated)
    return updated


async def delete_article(session: AsyncSession, article_id: int):
    article = await get_article_by_id_repo(session, article_id)

    if article is None:
        raise HTTPException(status_code=404, detail="Такого Артикуля нет")

    if article.is_deleted:
        raise HTTPException(status_code=404, detail="Артикул уже удален")

    delete = await delete_article_repo(session, article_id)
    await session.commit()
    return delete


async def upload_image(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Неверный тип данных")

    if file.size is not None and file.size > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Файл весит много")

    unique_name = await run_in_threadpool(upload_file, file.file, file.filename)
    return unique_name
