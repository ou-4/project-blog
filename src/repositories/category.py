from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_blog.models import Category


async def repo_get_categories(session: AsyncSession):
    res = await session.execute(select(Category))
    categories = res.scalars().all()
    return categories


async def repo_create_category(session: AsyncSession, name: str):
    new_category = Category(name=name)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


async def get_category_by_id(session: AsyncSession, category_id: int):
    category = await session.get(Category, category_id)
    return category
