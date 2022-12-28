import requests
from src.core.config import Settings


class MyRequests:
    """Этот класс отвечает за выполнение запросов к API"""

    @staticmethod
    def get(
        url: str, data: dict = None, headers: dict = None, cookies: dict = None
    ) -> requests.Response:
        """Отвечает за выполнение GET запросов

        Args:
            url (str): URL адрес
            data (dict, optional): Параметры запроса, по умолчанию None
            headers (dict, optional): Заголовки, по умолчанию None
            cookies (dict, optional): Cookie, по умолчанию None

        Returns:
            requests.Response: Тело ответа
        """
        return MyRequests._send(
            url=url, data=data, headers=headers, cookies=cookies, method="GET"
        )

    @staticmethod
    def post(
        url: str, data: dict = None, headers: dict = None, cookies: dict = None
    ) -> requests.Response:
        """Отвечает за выполнение POST запросов

        Args:
            url (str): URL адрес
            data (dict, optional): Параметры запроса, по умолчанию None
            headers (dict, optional): Заголовки, по умолчанию None
            cookies (dict, optional): Cookie, по умолчанию None

        Returns:
            requests.Response: Тело ответа
        """
        return MyRequests._send(
            url=url, data=data, headers=headers, cookies=cookies, method="POST"
        )

    @staticmethod
    def _send(
        url: str, data: dict, headers: dict, cookies: dict, method: str
    ) -> requests.Response:
        """Общий метод выполнения запросов

        Args:
            url (str): URL адрес
            data (dict): Параметры запроса
            headers (dict): Заголовки
            cookies (dict): Cookie
            method (str): Тип запроса

        Raises:
            Exception: Сработает, если метод является неверным

        Returns:
            requests.Response: Тело ответа
        """
        url = f"{Settings.TEST_URL}{url}"

        if method == "GET":
            response = requests.get(
                url=url, params=data, headers=headers, cookies=cookies
            )
        elif method == "POST":
            response = requests.post(
                url=url, data=data, headers=headers, cookies=cookies
            )
        else:
            raise Exception(f"Bad HTTP method {method} was received")

        return response
