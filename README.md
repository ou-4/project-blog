# project-blog

1. Первый коммит: Выполнены все необходимые подвязки, подготовлена структура проекта.
2. Финальный коммит
## Стек технологий

- Python 3.12
- FastAPI
- PostgreSQL + pgvector
- SQLAlchemy + Alembic
- RabbitMQ + Celery
- MinIO (S3)
- Ollama
- GROQ
- MailHog
- Docker + Docker Compose
- pytest

## Запуск через Docker

```bash
# Клонировать
git clone <url>
cd project-blog

# Скопировать .env
cp .env.example .env
# Заполнить своими значениями

# Запустить всё
docker compose up --build
```

# Применить миграции
make migrate

# Скачать модель эмбеддингов в Ollama
docker exec -it ollama ollama pull nomic-embed-text


API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`
MailHog: `http://localhost:8025`
MinIO Console: `http://localhost:9001`
RabbitMQ Management: `http://localhost:15672`

## Запуск тестов

```bash
# Создать тестовую БД
docker exec -it my_postgres psql -U bloguser -d postgres -c "CREATE DATABASE blogdb_test;"

# Запустить тесты
pytest
```

## Структура проекта

```
src/
├── project_blog/       # SQLAlchemy модели
├── schemas/            # Pydantic-схемы
├── repositories/       # Работа с БД
├── services/           # Бизнес-логика
├── routing/            # Эндпоинты
├── db/                 # Подключение к БД
├── config.py           # Настройки
├── middleware.py       # JWT middleware
├── worker.py           # Celery
└── main.py             # Точка входа
```

## Основные эндпоинты

- `POST /auth/register` — регистрация
- `POST /auth/login` — логин
- `GET /categories` — список категорий
- `POST /categories` — создать категорию
- `GET /articles` — список статей (пагинация, поиск, фильтр)
- `POST /articles` — создать статью
- `GET /articles/{id}` — одна статья
- `PUT /articles/{id}` — обновить
- `DELETE /articles/{id}` — удалить (мягко)
- `POST /articles/{id}/image` — загрузить картинку, получить image_key
- `POST /ai/ask` — задать вопрос по блогу (RAG)

AI-помощник (RAG)
Функционал умного Q&A по блогу:
1. При создании/обновлении статьи её текст отправляется в Celery-задачу index_article.
2. Воркер разбивает текст на чанки, считает эмбеддинги через Ollama и сохраняет их в PostgreSQL (pgvector).
3. Пользователь задаёт вопрос через POST /ai/ask.
4. Бэкенд считает эмбеддинг вопроса, ищет top-5 релевантных чанков, собирает контекст и отправляет в Groq LLM.
5. Возвращается ответ LLM + список статей-источников.

## Проверка через curl

### Регистрация

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Логин (сохраняет cookie)

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}' \
  -c cookies.txt
```

### Создать категорию

```bash
curl -X POST http://localhost:8000/categories/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"name": "Tech"}'
```

### Список категорий

```bash
curl http://localhost:8000/categories/
```

### Загрузить картинку

```bash
curl -X POST http://localhost:8000/articles/upload \
  -F "file=@/path/to/image.jpg" \
  -b cookies.txt
# → {"image_key": "uuid.png"}
```

### Создать статью

```bash
curl -X POST http://localhost:8000/articles/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title": "First Article", "content": "Hello world", "category_id": 1, "image_key": "uuid.png"}'
```

### Список статей с пагинацией

```bash
curl "http://localhost:8000/articles/?page_number=1&page_size=10"
```

### Поиск статей

```bash
curl "http://localhost:8000/articles/?search=hello"
```

### Фильтр по категории

```bash
curl "http://localhost:8000/articles/?category_id=1"
```

### Одна статья

```bash
curl http://localhost:8000/articles/1
```

### Обновить статью

```bash
curl -X PUT http://localhost:8000/articles/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title": "Updated Title"}'
```

### Удалить статью

```bash
curl -X DELETE http://localhost:8000/articles/1 -b cookies.txt
```

### Задать вопрос AI-помощнику (RAG)

```bash
curl -X POST http://localhost:8000/ai/ask \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"question": "What is FastAPI?"}'
```

Ответ:

```json
{
  "answer": "FastAPI is a modern Python web framework...",
  "sources": [
    {"article_id": 9, "title": "FastAPI intro", "image_url": "http://localhost:9000/articles/uuid.png"}
  ]
}
```
```
