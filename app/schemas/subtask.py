import datetime
from annotated_types import Gt, MaxLen
from pydantic import BaseModel, ConfigDict
from typing import Annotated

from app.utils.enum_schema import Status


class SubTaskCreate(BaseModel):
    order_number: Annotated[int, Gt(0)] | None = None
    title: Annotated[str, MaxLen(100)]
    status: Status = Status.not_completed


class SubTaskUpdate(BaseModel):
    order_number: Annotated[int, Gt(0)] | None = None
    title: Annotated[str, MaxLen(100)] | None = None
    status: Status | None = None


class SubTaskRead(BaseModel):
    id: int
    order_number: int
    title: str
    status: Status
    completed_at: datetime.datetime | None
    task_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
