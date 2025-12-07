from pydantic import BaseSettings

class Settings(BaseSettings):
    # General
    MODEL_DIR: str = "models"
    LOG_LEVEL: str = "INFO"

    # Postgres
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "reco"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # API / System
    TOP_K_DEFAULT: int = 10

settings = Settings()
