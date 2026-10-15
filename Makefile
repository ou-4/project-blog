.PHONY: migrate

migrate:
	docker compose exec app alembic upgrade head
