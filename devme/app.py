import asyncio

from aerich import Command
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_404_NOT_FOUND
from starlette.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from devme import caddy
from devme.constants import API_PREFIX
from devme.exceptions import (
    exception_handler,
    http_exception_handler,
    not_exists_exception_handler,
    validation_exception_handler,
)
from devme.routes import router
from devme.settings import TORTOISE_ORM, settings

if settings.debug:
    app = FastAPI(
        title="devme",
        description="Deploy your git project like a charm",
        contact={
            "name": "long2ice",
            "url": "https://github.com/long2ice/devme",
            "email": "jinlong.peng@merico.dev",
        },
        terms_of_service="https://github.com/long2ice",
        debug=settings.debug,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


else:
    app = FastAPI(
        debug=settings.debug,
        redoc_url=None,
        docs_url=None,
    )
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
)
app.include_router(router, prefix=API_PREFIX)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(DoesNotExist, not_exists_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

templates = Jinja2Templates(directory="static")


@app.exception_handler(StarletteHTTPException)
async def spa_server(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_404_NOT_FOUND and not request.scope["path"].startswith(API_PREFIX):
        return templates.TemplateResponse("index.html", context={"request": request})
    else:
        return await http_exception_handler(request, exc)


@app.on_event("startup")
async def startup():
    asyncio.ensure_future(caddy.start())
    aerich = Command(TORTOISE_ORM)
    await aerich.init()
    await aerich.upgrade()
