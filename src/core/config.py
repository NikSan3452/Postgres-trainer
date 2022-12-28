from dataclasses import dataclass


@dataclass
class Settings:

    # Секретный ключ. Заменить на надежный
    SECRET_KEY: str = "secret_key"
    # Время жизни токена
    TOKEN_EXPIRATION: int = 3600 * 24 * 30
    # Время жизни cookie
    COOKIE_EXPIRATION: int = 3600 * 24 * 30

    # Имя образа docker, этот параметр используется для создания контейнеров.
    # Если возникает ошибка "Errno: Name or service not known",
    # проверьте имя образа докер, оно должно совпадать с тем, что указано здесь,
    # если имя образа на вашем компьютере отличается, то нужно заменить
    # этот параметр на тот, что указан в вашем компьютере.
    DOCKER_IMAGE_NAME: str = "postgres-trainer_db"

    # Можно посмотреть командой: docker network ls.
    # Точно также, как и параметр выше - должно совпадать с указанным здесь.
    DOCKER_NETWORK: str = "postgres-trainer_default"

    # Тестовый url
    TEST_URL:str = "http://127.0.0.1:8000/"
