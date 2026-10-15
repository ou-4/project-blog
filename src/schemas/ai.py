from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class SourceOut(BaseModel):
    article_id: int
    title: str
    image_url: str | None


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceOut]
