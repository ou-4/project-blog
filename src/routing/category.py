from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.category import CategoryCreate, CategoryOut
from src.services.category import create_category, get_categories

router_category = APIRouter(prefix="/categories", tags=["categories"])


@router_category.get("/", response_model=list[CategoryOut])
async def get_cats(session: AsyncSession = Depends(get_db)):
    return await get_categories(session)


@router_category.post("/", response_model=CategoryOut)
async def create_cats(data: CategoryCreate, session: AsyncSession = Depends(get_db)):
    return await create_category(session, data.name)
