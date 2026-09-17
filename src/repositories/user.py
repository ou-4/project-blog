from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.project_blog.models import User


async def get_user_by_email(session: AsyncSession, email: str):
    res = await session.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    return user


async def create_user(session: AsyncSession, email: str, password: str):
    new_user = User(email=email, password=password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
