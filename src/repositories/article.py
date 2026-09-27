from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_blog.models import Article


async def create_article_repo(
    session: AsyncSession, title: str, content: str, category_id: int, image_url: str | None = None
):
    article = Article(title=title, content=content, category_id=category_id, image_url=image_url)
    session.add(article)
    await session.flush()
    return article


async def get_articles_repo(
    session: AsyncSession,
    page_number: int,
    page_size: int,
    category_id: int | None = None,
    search: str | None = None,
):
    query = select(Article).where(Article.is_deleted.is_(False))

    if category_id is not None:
        query = query.where(Article.category_id == category_id)

    if search is not None:
        search_query = func.plainto_tsquery("russian", search)
        document = func.to_tsvector("russian", Article.title + " " + Article.content)
        query = query.where(document.op("@@")(search_query))

    offset = (page_number - 1) * page_size
    total_query = await session.execute(select(func.count()).select_from(query.subquery()))
    res = await session.execute(
        query.order_by(Article.created_at.desc(), Article.id.desc()).limit(page_size).offset(offset)
    )
    total = total_query.scalar()
    articles = res.scalars().all()
    return articles, total


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
        return None

    if title is not None:
        article.title = title

    if content is not None:
        article.content = content

    if category_id is not None:
        article.category_id = category_id

    if image_url is not None:
        article.image_url = image_url

    await session.flush()
    return article


async def delete_article_repo(session: AsyncSession, article_id: int):
    article = await session.get(Article, article_id)
    if article is None:
        return None

    article.is_deleted = True
    await session.flush()
    return {"succes": True}
