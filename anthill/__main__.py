from fastapi import FastAPI, Body, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from uuid import uuid4
from datetime import datetime, UTC
import logging
import uvicorn
from typing import Annotated
import asyncio
from anthill import schemas, config
from anthill.exception_handler import handle_http_exception
from anthill.exception_handler import handle_unhandled_exception
from anthill.exception_handler import handle_validation_exception


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


app = FastAPI()


runs: list[schemas.Run] = []


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return await handle_unhandled_exception(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return await handle_http_exception(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,
                                       exc: RequestValidationError):
    return await handle_validation_exception(request, exc)


@app.post("/api/v1/srv/runs/")
async def create_run(
    job_id: Annotated[int, Body()],
    code: Annotated[str, Body()],
    external_status: Annotated[str, Body()],
    start_time: Annotated[datetime, Body()]
) -> schemas.Run:
    now = datetime.now(UTC)
    run = schemas.Run(
        run_id=uuid4(),
        job_id=job_id,
        external_status=external_status,
        start_time=start_time,
        created_at=now,
        updated_at=now,
        status=schemas.RunStatus.CREATED
    )
    runs.append(run)
    return run


@app.get("/api/v1/srv/runs/")
async def get_runs() -> list[schemas.Run]:
    return runs


async def main():
    server_config = config.create_server_config()
    uvicorn.run("anthill.__main__:app",
                host=server_config.host,
                port=server_config.port,
                reload=server_config.debug)


if __name__ == "__main__":
    asyncio.run(main())
