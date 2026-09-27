from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    SECRET_KEY: str
    MINIO_PUBLIC_URL: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str
    MINIO_BUCKET: str
    CELERY_BROKER_URL: str
    COOKIE_SECURE: bool
    model_config = {"env_file": ".env", "extra": "ignore"}


class TestSettings(BaseSettings):
    TEST_DATABASE_URL: str
    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
test_settings = TestSettings()
