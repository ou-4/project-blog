from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_blog.models import Article


async def create_article_repo(
    session: AsyncSession, title: str, content: str, category_id: int, image_url: str | None = None
):
    article = Article(title=title, content=content, category_id=category_id, image_url=image_url)
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article


async def get_articles_repo(
    session: AsyncSession,
    page_number: int,
    page_size: int,
    category_id: int | None = None,
    search: str | None = None,
):
    query = select(Article)

    if category_id is not None:
        query = query.where(Article.category_id == category_id)

    if search is not None:
        search_query = func.plainto_tsquery(search)
        query = query.where(
            func.to_tsvector(Article.title).op("@@")(search_query)
            | func.to_tsvector(Article.content).op("@@")(search_query)
        )

    offset = (page_number - 1) * page_size
    res = await session.execute(query.limit(page_size).offset(offset))
    articles = res.scalars().all()
    return articles


async def get_article_by_id_repo(session: AsyncSession, id: int):
    res = await session.execute(select(Article).where(Article.id == id))
    article = res.scalar_one_or_none()
    return article


async def update_article_repo(
    session: AsyncSession,
    article_id: int,
    title: str | None,
    content: str | None,
    category_id: int | None,
    image_url: str | None,
):
    article = await session.get(Article, article_id)

    if article is None:
        raise HTTPException(status_code=409, detail="Такого id Артикула нет")

    if title is not None:
        article.title = title

    if content is not None:
        article.content = content

    if category_id is not None:
        article.category_id = category_id

    if image_url is not None:
        article.image_url = image_url

    await session.commit()
    await session.refresh(article)
    return article


async def delete_article_repo(session: AsyncSession, article_id: int):
    article = await session.get(Article, article_id)
    if article is None:
        raise HTTPException(status_code=409, detail="Такого id Артикула нет")

    article.is_deleted = True
    await session.commit()
    return {"succes": True}
