from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.ai import AskRequest, AskResponse
from src.services.ai import ask_question

router_ai = APIRouter(prefix="/ai", tags=["ai"])


@router_ai.post("/ask", response_model=AskResponse)
async def ai(question: AskRequest, session: AsyncSession = Depends(get_db)):
    return await ask_question(session, question.question)
