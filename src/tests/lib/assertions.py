import requests


class Assertions:
    """Этот класс отвечает за все assert"""

    @staticmethod
    def assert_code_status(
        response: requests.Response, expected_status_code: int
    ) -> None:
        """Отвечает за проверку кода ответа

        Args:
            response (requests.Response): Тело ответа
            expected_status_code (int): Ожидаемый код ответа
        """
        assert (
            response.status_code == expected_status_code
        ), f"Неожиданный код ответа, ожидалось {expected_status_code}, получили {response.status_code}"

    @staticmethod
    def assert_cookie_exists(response: requests.Response) -> None:
        """Отвечает за проверку наличия файла cookie

        Args:
            response (requests.Response): Тело ответа
        """
        assert "trainer" in response.cookies, f"Файл cookie отсутствует"

    @staticmethod
    def assert_cookie_missing(response: requests.Response) -> None:
        """Отвечает за проверку отсуствия файла cookie

        Args:
            response (requests.Response): Тело ответа
        """
        assert (
            "trainer" not in response.cookies
        ), f"Файл cookie существует хотя не должен"

    @staticmethod
    def assert_wrong_server_response(response: requests.Response) -> None:
        """Отвечает за проверку ответов сервера

        Args:
            response (requests.Response): Тело ответа
        """
        assert "Ошибка" not in response.text, "Неверный ответ сервера"
