# project-blog

1. Первый коммит: Выполнены все необходимые подвязки, подготовлена структура проекта.
2. Финальный коммит
## Стек технологий

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- RabbitMQ + Celery
- MinIO (S3)
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

API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`

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
- `POST /articles/{id}/image` — загрузить картинку

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
  -d '{"name": "Tech"}'
```

### Список категорий

```bash
curl http://localhost:8000/categories/
```

### Создать статью

```bash
curl -X POST http://localhost:8000/articles/ \
  -H "Content-Type: application/json" \
  -d '{"title": "First Article", "content": "Hello world", "category_id": 1}'
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
  -d '{"title": "Updated Title"}'
```

### Удалить статью

```bash
curl -X DELETE http://localhost:8000/articles/1
```

### Загрузить картинку

```bash
curl -X POST http://localhost:8000/articles/1/image \
  -F "file=@/path/to/image.jpg"
```

### Защищённый эндпоинт (с cookie)

```bash
curl -X POST http://localhost:8000/articles/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title": "Auth Article", "content": "Text", "category_id": 1}'
```
