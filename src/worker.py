from celery import Celery

from src.config import settings

app = Celery("tasks", broker=settings.CELERY_BROKER_URL)


@app.task
def send_welcome_email(email: str):
    print(f"Отправлено письмо на {email}")
