import bcrypt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user import create_user, get_user_by_email
from src.schemas.user import UserCreate, UserLogin
from src.worker import send_welcome_email


async def register_user(session: AsyncSession, data: UserCreate):
    user = await get_user_by_email(session, data.email)

    if user is None:
        hashed_pswd = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        new_user = await create_user(session, data.email, hashed_pswd)
        send_welcome_email.delay(data.email)
        return new_user
    else:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")


def check_pswd(password, hashed_pswd):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_pswd.encode("utf-8"))


async def authenticate_user(session: AsyncSession, data: UserLogin):
    user = await get_user_by_email(session, data.email)

    if user is None:
        raise HTTPException(
            status_code=401, detail="Пользователь с таким email уже существует или еще не создан"
        )

    pswd = data.password
    hashed_pswd = user.password

    if check_pswd(pswd, hashed_pswd):
        return user
    else:
        raise HTTPException(status_code=401, detail="Пароль неправильный")
