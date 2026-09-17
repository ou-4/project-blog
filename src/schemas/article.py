from datetime import datetime

from fastapi import Query
from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str
    category_id: int
    image_url: str | None = None


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category_id: int | None = None
    image_url: str | None = None


class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    category_id: int
    image_url: str | None
    created_at: datetime
    updated_at: datetime


class ArticleListParams(BaseModel):
    search: str | None = Query(None)
    category_id: int | None = Query(None)
    page_number: int = Query(1, ge=1)
    page_size: int = Query(10, ge=1, le=100)
