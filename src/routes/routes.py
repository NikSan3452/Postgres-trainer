from typing import Optional
from fastapi import status, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request

import exceptions as exc
from core.config import tmp, Settings
from dockerization.container import crud
from db.db import db


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    """Отвечает за отображение главной страницы

    Args:
        request (Request): Тело запроса

    Returns:
        _type_: HTML - ответ
    """
    return tmp.TemplateResponse("main.html", context={"request": request})


@router.post("/run", response_class=HTMLResponse)
async def main(request: Request) -> HTMLResponse:
    """Отвечает за обработку запросов к базе данных.
    Функция получает токен из cookie, декодирует его
    и получает url БД, к которой необходимо подключиться.
    Этот url был автоматически сгенерирован для
    конкретного пользователя. Из тела зпроса
    извлекается sql - запрос к БД и в зависимости от
    его типа передается соотвествующему методу.

    Args:
        request (Request): Тело запроса

    Returns:
        HTMLResponse: HTML - ответ
    """
    
    # Получаем токен из cookie
    cookie_exists = request.cookies.get("trainer")
    if not cookie_exists:
        return JSONResponse(
            content="База данных не создана", status_code=status.HTTP_409_CONFLICT
        )

    # Декодируем токен
    decoded_token = crud.decode_token(token=cookie_exists)
    # Извлекаем url базы данных
    db_url = decoded_token.split(":::")[1]

    # Получем тело запроса
    json = await request.json()
    # Извлекаем строку sql - запроса
    query = json.get("data")
    query = query.lower()

    error = None
    msg = None

    # Если тип запроса select
    if (
        "select" in query
        and "create" not in query
        and "insert" not in query
        and "update" not in query
        and "delete" not in query
    ):  
        # Вызываем функцию отвечающую за select запросы
        result = await db.run_select_queries(query=query, db_url=db_url)
        if "Ошибка" in result:
            error = result

        # Получем имена столбцов из результатов запроса
        table_headers = result[0]
        # Получем сами результаты
        query_results = result[1]

        return tmp.TemplateResponse(
            "table.html",
            context={
                "request": request,
                "query_results": query_results,
                "model_headers": table_headers,
                "error": error,
            },
        )

    # Если тип запроса отличный от select
    if "create" in query or "insert" in query or "update" in query or "delete" in query:
        # Вызываем функцию отвечающую за соотвествующие запросы
        result = await db.get_other_queries(query=query, db_url=db_url)
        if "Ошибка" in result:
            error = result
        if result == "Выполнено":
            msg = result

        return tmp.TemplateResponse(
            "table.html",
            context={"request": request, "error": error, "msg": msg},
        )


@router.post("/new-database", response_class=JSONResponse)
def create(request: Request) -> Optional[JSONResponse]:
    """Отвечает за обработку запросов на создание контейнеров.
    Если cookie не существует, значит контейнер не создан,
    тогда функция create_container попытается создать новый
    контейнер и вернет его имя. Метод ecoded_token создаст
    токен с именем контейнера. Метод set_cookie установит
    cookie.

    Args:
        request (Request): Тело запроса

    Raises:
        exc.DockerException: Сработает если по каким-то причинам
        не удалось создать новый контейнер

    Returns:
        Optional[JSONResponse]: JSON - ответ
    """
    # Если cookie не существует
    cookie_exists = request.cookies.get("trainer")
    if not cookie_exists:
        try:
            # Формируем тело ответа
            response = JSONResponse(
                content="Новая база данных успешно создана",
                status_code=status.HTTP_200_OK,
            )

            # Создаем контейнер и получем его имя
            container_name = crud.create_container()
            # Кодируем имя контейнера
            encoded_container = crud.encode_token(obj=container_name)

            # Устанавливаем cookie с токеном клиенту
            response.set_cookie(
                key="trainer",
                value=encoded_container,
                expires=Settings.COOKIE_EXPIRATION,
                httponly=True,
                samesite="lax",
            )
            return response
        except Exception as exc:
            return f"{exc} Неудалось создать базу данных"
    else:
        return JSONResponse(
            content="База данных уже создана", status_code=status.HTTP_200_OK
        )


@router.post("/delete", response_class=JSONResponse)
def delete(request: Request) -> Optional[JSONResponse]:
    """Отвечает за обработку запросов на удаление контейнеров.
    Если файл cookie существует - извлекает из него токен,
    метод decode_token декодирует его и получает имя контейнера,
    необходимое для метода remove_container, этот метод в свою очередь
    удалит необходимый контейнер. Метод delete_cookie - удалит cookie.

    Args:
        request (Request): Тело запроса

    Raises:
        exc.DockerException: Сработает если база данных не была создана

    Returns:
        Optional[JSONResponse]: JSON - ответ
    """
    # Если cookie существует извлекаем токен
    cookie_exists = request.cookies.get("trainer")
    if not cookie_exists:
        return JSONResponse(
            content="База данных не создана", status_code=status.HTTP_409_CONFLICT
        )
    try:
        # Формируем тело ответа
        response = JSONResponse(
            content="База данных удалена", status_code=status.HTTP_200_OK
        )
        # Декодируем токен
        decoded_token = crud.decode_token(token=cookie_exists)
        # Извлекаем имя контейнера
        decoded_token = decoded_token.split(":::")[0]
        # Удаляем контейнер
        crud.remove_container(name=decoded_token)
        # Удаляем cookie
        response.delete_cookie(key="trainer")
        return response
    except Exception as exc:
        return f"{exc} Неудалось удалить базу данных"
