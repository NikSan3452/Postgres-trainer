import pathlib
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from exceptions import exceptions as exc

from routes.routes import router
from dockerization.container import crud
from core.config import Settings

exception_handlers = {
    404: exc.not_found_error,
    500: exc.internal_error,
}


app = FastAPI(exception_handlers=exception_handlers, title=Settings.PROJECT_NAME)

app.mount(
    "/static",
    StaticFiles(
        directory=pathlib.Path(__file__).parent.parent.absolute() / "./src/static"
    ),
    name="static",
)

app.include_router(router)


@app.on_event('shutdown') 
def stop() -> None:
    crud.remove_all_containers()