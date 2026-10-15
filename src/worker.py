import asyncio
from email.mime.text import MIMEText
import smtplib

from celery import Celery
from sqlalchemy import delete

from src.config import settings
from src.db.session import AsyncSessionLocal
from src.project_blog.models import Article, ArticleChunk
from src.services.chunking import chunk_text
from src.services.llm import embed

app = Celery("tasks", broker=settings.CELERY_BROKER_URL)


@app.task
def send_welcome_email(email: str):
    message = MIMEText("Привет!")
    message["Subject"] = "Тема"
    message["From"] = "sender@example.com"
    message["To"] = "recipient@example.com"

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.send_message(message)


@app.task
def index_article(article_id: int):
    asyncio.run(_index_article(article_id))


async def _index_article(article_id: int):
    async with AsyncSessionLocal() as session:
        article = await session.get(Article, article_id)
        if article is None or article.is_deleted:
            return

        await session.execute(delete(ArticleChunk).where(ArticleChunk.article_id == article_id))

        text = article.title + "\n\n" + article.content
        chunks = chunk_text(text)

        for chunk_content in chunks:
            vector = await embed(chunk_content)
            article_chunk = ArticleChunk(
                article_id=article_id,
                content=chunk_content,
                embedding=vector,
            )
            session.add(article_chunk)

        await session.commit()
