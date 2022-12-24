from fastapi.templating import Jinja2Templates

class Settings:
    SECRET_KEY: str = 'secret_key'
    ALGORITHM: str = "HS256"

    TOKEN_EXPIRATION: int = 3600 * 12
    COOKIE_EXPIRATION: int = 3600 * 12

    DOCKER_IMAGE_NAME: str = "postgres-trainer-db"
    # Можно посмотреть командой: docker network ls
    DOCKER_NETWORK: str = "postgres-trainer_default" 

tmp = Jinja2Templates(directory="templates") 