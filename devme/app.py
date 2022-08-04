import asyncio

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
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
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(DoesNotExist, not_exists_exception_handler)


@app.on_event("startup")
async def startup():
    asyncio.ensure_future(caddy.start())
