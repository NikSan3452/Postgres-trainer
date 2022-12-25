import docker
import uuid
import secrets
import string
import random

from typing import Optional
from itsdangerous import URLSafeTimedSerializer
from core.config import Settings


client = docker.from_env()


class ContainerCrud:
    """Этот класс отвечает за создание и управление контейнерами docker"""

    def __init__(self) -> None:
        self.container_name: str = None
        self.container_port: int = None
        self.container_port_list: list[int] = []

        self.postgres_user: str = None
        self.postgres_password: str = None
        self.postgres_server: str = None
        self.postgres_port: int = None
        self.postgres_db: str = None
        self.database_url: str = None

    def create_container(self) -> Optional[str]:
        """Отвечает за создание контейнера Docker

        Returns:
            str: Имя контейнера
        """
        self.container_name = self.create_container_name()
        self.container_port = self.create_container_port()
        self.database_url = self.create_db_url()
        
        try:
            container = client.containers.create(
                image=Settings.DOCKER_IMAGE_NAME,
                auto_remove=True,
                name=self.container_name,
                environment={
                    "POSTGRES_USER": self.postgres_user,
                    "POSTGRES_PASSWORD": self.postgres_password,
                    "POSTGRES_SERVER": self.postgres_server,
                    "POSTGRES_PORT": self.container_port,
                    "POSTGRES_DB": self.postgres_db,
                },
                network=Settings.DOCKER_NETWORK,
                ports={"5432/tcp": self.container_port},
                publish_all_ports=True,
            )
            print(container)
            # Сразу же запускаем контейнер
            container.start()
            return container.name

        except Exception as exc:
            return f"Ошибка: {exc} Не удалось создать контейнер"

    def remove_container(self, name: str) -> None:
        """Отвечает за остановку контейнеров Docker,
        т.к при создании контейнеров установлен флаг
        auto_remove = True, это приводит к удалению
        контейнеров

        Args:
            name (str): Имя контейнера
        """
        try:
            container = client.containers.get(name)
            container.stop()
        except Exception as exc:
            return f"Ошибка: {exc} Не удалось остановить контейнер"
    
    def remove_all_containers(self):
        try:
            for container in client.containers.list():
                container.remove()
        except Exception as exc:
            return f"Ошибка: {exc} Не удалось остановить контейнер"

    def create_container_name(self) -> str:
        """Отвечает за генерацию уникальных имен контейнеров Docker

        Returns:
            str: Имя контейнера Docker
        """
        self.container_name = str(uuid.uuid4())
        return self.container_name

    def create_container_port(self) -> int:
        """Отвечает за генерацию случайного порта контейнера Docker

        Returns:
            int: Порт
        """
        self.container_port = random.randint(1000, 65000)
        if self.container_port not in self.container_port_list:
            self.container_port_list.append(self.container_port)
        return self.container_port

    def create_db_url(self) -> str:
        """Отвечает за генерацию рандомных данных,
        которые используются для создания нового url,
        используемого для подключения к БД

        Returns:
            str: URL для подключения к БД
        """
        self.postgres_user = "".join(
            secrets.choice(string.ascii_letters) for _ in range(8)
        )
        self.postgres_password = "".join(
            secrets.choice(string.ascii_letters + string.digits) for i in range(12)
        )
        self.postgres_server = self.container_name
        self.postgres_port = 5432
        self.postgres_db = "".join(
            secrets.choice(string.ascii_letters) for _ in range(12)
        )
        self.database_url = f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        return self.database_url

    def encode_token(self, obj: str) -> str:
        """Отвечает за создание токена

        Args:
            obj (str): Объект, который необходимо закодировать

        Returns:
            str: Токен
        """
        serializer = URLSafeTimedSerializer(Settings.SECRET_KEY)
        url = obj + ":::" + self.database_url
        return serializer.dumps(url, salt="trainer-cookie-salt")

    def decode_token(
        self, token: str, expiration: Optional[int] = Settings.TOKEN_EXPIRATION
    ) -> Optional[str]:
        """Декодирует токен

        Args:
            token (str): Токен
            expiration (int, optional): Время истечения срока действия токена

        Returns:
            str: Содержимое токена
        """
        serializer = URLSafeTimedSerializer(Settings.SECRET_KEY)
        try:
            payload = serializer.loads(
                token, salt="trainer-cookie-salt", max_age=expiration
            )
            return payload
        except Exception:
            return False


crud = ContainerCrud()
