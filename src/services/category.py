from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.category import repo_create_category, repo_get_categories


async def get_categories(session: AsyncSession):
    return await repo_get_categories(session)


async def create_category(session: AsyncSession, name: str):
    categories = await repo_get_categories(session)
    if name not in [cat.name for cat in categories]:
        new_category = await repo_create_category(session, name)
        await session.commit()
        return new_category

    raise HTTPException(status_code=409, detail="Такая категория уже существует")
