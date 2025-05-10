import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)


async def handle_unhandled_exception(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"})


async def handle_http_exception(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        logger.warning("http exception: [%s] %s", exc.status_code, exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
    raise exc


async def handle_validation_exception(request: Request, exc: Exception):
    if isinstance(exc, RequestValidationError):
        logger.warning("validation error: [%s] %s", exc.errors())
        return JSONResponse(
            status_code=422,
            content={"message": "Validation error", "detail": exc.errors()}
        )
    raise exc
