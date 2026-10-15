from sqlalchemy.ext.asyncio import AsyncSession

from src.project_blog.models import Article
from src.repositories.chunk import search_similar_chunks
from src.schemas.ai import AskResponse, SourceOut
from src.services.llm import embed, generate


async def ask_question(session: AsyncSession, question: str):
    vector = await embed(question)
    chunks = await search_similar_chunks(session, vector, limit=5)

    if not chunks:
        return AskResponse(answer="No relevant articles found", sources=[])

    context = "\n\n".join([chunk.content for chunk in chunks])
    prompt = (
        f"Answer the question based on the context.\n\nContext:\n{context}\n\nQuestion: {question}"
    )
    answer = await generate(prompt)

    articles_id = {chunk.article_id for chunk in chunks}

    sources = []
    for article_id in articles_id:
        article = await session.get(Article, article_id)
        if article is not None:
            sources.append(
                SourceOut(article_id=article.id, title=article.title, image_url=article.image_url)
            )

    return AskResponse(answer=answer, sources=sources)
