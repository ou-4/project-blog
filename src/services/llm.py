import httpx
from openai import OpenAI

from src.config import settings


async def embed(text: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.OLLAMA_URL}/api/embed"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "input": text,
        }
        response = await client.post(url, json=payload)
        return response.json()["embeddings"][0]


client = OpenAI(api_key=settings.GROQ_API_KEY, base_url=settings.GROQ_URL)


def generate(prompt: str):
    client = OpenAI(api_key=settings.GROQ_API_KEY, base_url=settings.GROQ_URL)
    response = client.responses.create(
        input=prompt,
        model=settings.GROQ_MODEL,
    )
    return response.output_text
