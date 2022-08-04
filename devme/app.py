import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler as exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_404_NOT_FOUND
from starlette.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from devme import caddy
from devme.exceptions import http_exception_handler, not_exists_exception_handler
from devme.routes import router
from devme.settings import settings

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
else:
    app = FastAPI()
register_tortoise(
    app,
    db_url=settings.db_url,
    modules={"models": ["devme.models"]},
    generate_schemas=True,
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.include_router(router, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(DoesNotExist, not_exists_exception_handler)

templates = Jinja2Templates(directory="static")


@app.exception_handler(StarletteHTTPException)
async def spa_server(request: Request, exc: StarletteHTTPException):
    if exc.status_code == HTTP_404_NOT_FOUND:
        return templates.TemplateResponse("index.html", context={"request": request})
    else:
        return await exception_handler(request, exc)


@app.on_event("startup")
async def startup():
    asyncio.ensure_future(caddy.start())
