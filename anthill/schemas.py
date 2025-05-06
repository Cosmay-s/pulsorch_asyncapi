from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
import enum


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
