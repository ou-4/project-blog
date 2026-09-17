from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.user import UserCreate, UserLogin, UserOut
from src.services.auth import create_access_token
from src.services.user import authenticate_user, register_user

router_auth = APIRouter(prefix="/auth", tags=["auth"])


@router_auth.post("/register", response_model=UserOut)
async def register(data: UserCreate, session: AsyncSession = Depends(get_db)):
    return await register_user(session, data)


@router_auth.post("/login", response_model=UserOut)
async def login(data: UserLogin, response: Response, session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(session, data)
    token = create_access_token(user.id)
    response.set_cookie("access_token", token)
    return user
