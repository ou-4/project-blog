from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.article import ArticleCreate, ArticleListParams, ArticleOut, ArticleUpdate
from src.services.article import (
    create_article as create_article_serv,
    delete_article as delete_article_serv,
    get_article_by_id,
    get_articles as get_articles_serv,
    update_article as update_article_serv,
    upload_article_image,
)

router_article = APIRouter(prefix="/articles", tags=["articles"])


@router_article.get("/")
async def get_articles(
    pagination: ArticleListParams = Depends(), session: AsyncSession = Depends(get_db)
):
    return await get_articles_serv(
        session,
        pagination.page_number,
        pagination.page_size,
        pagination.category_id,
        pagination.search,
    )


@router_article.get("/{article_id}", response_model=ArticleOut)
async def get_article(article_id: int, session: AsyncSession = Depends(get_db)):
    return await get_article_by_id(session, article_id)


@router_article.post("/", response_model=ArticleOut)
async def create_article(data: ArticleCreate, session: AsyncSession = Depends(get_db)):
    return await create_article_serv(
        session, data.title, data.content, data.category_id, data.image_url
    )


@router_article.put("/{article_id}", response_model=ArticleOut)
async def update_article(
    article_id: int, data: ArticleUpdate, session: AsyncSession = Depends(get_db)
):
    return await update_article_serv(
        session, article_id, data.title, data.content, data.category_id, data.image_url
    )


@router_article.delete("/{article_id}")
async def delete_article(article_id: int, session: AsyncSession = Depends(get_db)):
    return await delete_article_serv(session, article_id)


@router_article.post("/{article_id}/image", response_model=ArticleOut)
async def upload_image(
    article_id: int, file: UploadFile = File(...), session: AsyncSession = Depends(get_db)
):
    return await upload_article_image(session, article_id, file)
