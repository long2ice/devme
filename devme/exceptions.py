from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from tortoise.exceptions import DoesNotExist


class AddServerError(Exception):
    pass


class GetGitReposError(Exception):
    pass


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


async def not_exists_exception_handler(request: Request, exc: DoesNotExist):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"error": str(exc)},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": str(exc)},
    )
