from pathlib import Path
from tempfile import gettempdir
from pydantic_settings import BaseSettings

TEMP_DIR = Path(gettempdir())

class Settings(BaseSettings):
    # GENERAL
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development" # development, production
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = True
    WORKERS: int = 4
    WORKERS_TIMEOUT: int = 500
    API_V1_STR: str = "/api"
    STORAGE: str = "public"
    PROJECT_NAME: str = "ABC Platform"
    HOST: str = '0.0.0.0'
    PORT: int = 3000
    PROMETHEUS_DIR: Path = TEMP_DIR / "prom"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
