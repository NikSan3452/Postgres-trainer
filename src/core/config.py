from fastapi.templating import Jinja2Templates

class Settings:
    SECRET_KEY: str = 'secret_key'
    TOKEN_EXPIRATION: int = 3600 * 24 * 30
    COOKIE_EXPIRATION: int = 3600 * 24 * 30

    DOCKER_IMAGE_NAME: str = "postgres-trainer_db"
    # Можно посмотреть командой: docker network ls
    DOCKER_NETWORK: str = "postgres-trainer_default" 

tmp = Jinja2Templates(directory="templates") 