from fastapi import FastAPI, Body
from uuid import uuid4
from datetime import datetime, UTC
import logging
import uvicorn
from anthill import schemas, config
from typing import Annotated
import asyncio

app = FastAPI()
logger = logging.getLogger(__name__)
runs: list[schemas.Run] = []


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