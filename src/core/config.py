import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    SITE_KEY: str = os.getenv("SITE_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"

    TOKEN_EXPIRATION: int = 3600 * 12
    COOKIE_EXPIRATION: int = 3600 * 12

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    DOCKER_IMAGE_NAME: str = "postgres-trainer-db:latest"

    DOCKER_NETWORK: str = "postgres-trainer"


tmp = Jinja2Templates(directory="templates")
