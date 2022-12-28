import json

from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestApi:
    def test_api(self) -> None:
        """Общий метод для тестирования всех конечных точек API"""
        query = {"query": "select * from employees;"}
        query = json.dumps(query)

        # СОЗДАНИЕ НОВОЙ БАЗЫ ДАННЫХ
        response1 = MyRequests.post(url="new-database")
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_cookie_exists(response1)

        cookie = response1.cookies.get(name="trainer")

        # ВЫПОЛНЕНИЕ ЗАПРОСОВ К БАЗЕ ДАННЫХ
        response2 = MyRequests.post(url="run", data=query, cookies={"trainer": cookie})
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_wrong_server_response(response2)

        # УДАЛЕНИЕ COOKIE
        response3 = MyRequests.post(url="delete", cookies={"trainer": cookie})
        Assertions.assert_code_status(response3, 200)

        # ПРОВЕРКА ДЕЙСТВИТЕЛЬНО ЛИ COOKIE УДАЛЕН
        response4 = MyRequests.post(url="delete")
        Assertions.assert_code_status(response4, 409)
        Assertions.assert_cookie_missing(response4)
