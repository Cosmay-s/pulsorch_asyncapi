from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict
from uuid import UUID, uuid4
from datetime import datetime, UTC
import enum
import asyncio
import logging
from dotenv import load_dotenv
import os
import uvicorn

app = FastAPI()
logger = logging.getLogger(__name__)
load_dotenv()

class RunStatus(enum.Enum):
    CREATED = "created"
    SCHEDULED = "scheduled"


class Run(BaseModel):
    run_id: UUID
    job_id: int
    external_status: str
    start_time: datetime
    created_at: datetime
    updated_at: datetime
    status: RunStatus


class RunCreate(BaseModel):
    job_id: int
    external_status: str
    start_time: datetime

    model_config = ConfigDict(from_attributes=True)


runs: list[Run] = []


@app.post("/api/v1/srv/runs/", response_model=Run)
async def create_run(request: Request):
    try:
        json_run = await request.json()
        if not json_run:
            raise HTTPException(status_code=400, detail="Invalid JSON body")
        run_data = RunCreate(**json_run)
        logger.debug(f"Valided data: {run_data}")
        now = datetime.now(tz=UTC)
        run_uuid = uuid4()
        run = Run(
                run_id=run_uuid,
                job_id=run_data.job_id,
                external_status=run_data.external_status,
                start_time=run_data.start_time,
                created_at=now,
                updated_at=now,
                status=RunStatus.CREATED
            )
        runs.append(run)
        return run
    except ValueError as ve:
        logger.error(f"Value error: {ve}")
        raise HTTPException(status_code=400, detail="Value failed")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@app.get("/api/v1/srv/runs/", response_model=list[Run])
async def get_runs():
    return runs


HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8080"))
DEBUG = os.getenv("DEBUG", "True") == "True"


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)