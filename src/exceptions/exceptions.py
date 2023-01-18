from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, HTTPException, status

from endpoints.endpoints import tmp

exc_app = FastAPI()


def not_found_error(request: Request, exc: HTTPException) -> HTMLResponse:
    return tmp.TemplateResponse(
        "exceptions.html",
        {"request": request, "error": exc.detail},
        status_code=status.HTTP_404_NOT_FOUND,
    )


def internal_error(request: Request, exc: HTTPException) -> HTMLResponse:
    return tmp.TemplateResponse(
        "exceptions.html",
        {"request": request, "error": "Сервер столкнулся с непредвиденной ошибкой"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
