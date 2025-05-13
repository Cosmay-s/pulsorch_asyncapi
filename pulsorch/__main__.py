from fastapi import FastAPI, Body
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from uuid import uuid4
from datetime import datetime, UTC
import logging
import uvicorn
from typing import Annotated
import asyncio
from pulsorch import schemas, config
from pulsorch.exception_handler import handle_http_exception
from pulsorch.exception_handler import handle_unhandled_exception
from pulsorch.exception_handler import handle_validation_exception


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


app = FastAPI()


runs: list[schemas.Run] = []


app.add_exception_handler(Exception, handle_unhandled_exception)
app.add_exception_handler(HTTPException, handle_http_exception)
app.add_exception_handler(RequestValidationError, handle_validation_exception)


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
