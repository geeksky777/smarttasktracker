import datetime
from typing import Annotated
from annotated_types import Gt, MaxLen
from pydantic import BaseModel, ConfigDict


from app.utils.enum_schema import Status


class TaskCreate(BaseModel):
    order_number: Annotated[int, Gt(0)] | None = None
    title: Annotated[str, MaxLen(100)]
    description: Annotated[str, MaxLen(500)] | None = None
    status: Status = Status.not_completed


class TaskUpdate(BaseModel):
    order_number: Annotated[int, Gt(0)] | None = None
    title: Annotated[str, MaxLen(100)] | None = None
    description: str | None = None
    status: Status | None = None


class TaskRead(BaseModel):
    id: int
    order_number: int
    title: str
    description: str | None
    status: Status
    completed_at: datetime.datetime | None
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
