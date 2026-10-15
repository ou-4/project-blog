from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_blog.models import ArticleChunk


async def search_similar_chunks(
    session: AsyncSession, query_embedding: list[float], limit: int = 5
):
    stmt = (
        select(ArticleChunk)
        .order_by(ArticleChunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    res = await session.execute(stmt)
    return res.scalars().all()
