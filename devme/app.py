from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from devme import caddy
from devme.routes import router
from devme.settings import settings

app = FastAPI(
    title="devme",
    description="Deploy your git project like a charm",
    contact={
        "name": "long2ice",
        "url": "https://github.com/long2ice/devme",
        "email": "jinlong.peng@merico.dev",
    },
    terms_of_service="https://github.com/long2ice",
)
register_tortoise(
    app,
    db_url=settings.db_url,
    modules={"models": ["devme.models"]},
    generate_schemas=True,
)
app.include_router(router)


@app.on_event("startup")
async def startup():
    await caddy.start()


@app.on_event("shutdown")
async def startup():
    pass
