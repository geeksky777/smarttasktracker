from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Annotated


class UserCreate(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(50)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(50)]


class UserUpdate(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(50)] | None = None
    email: EmailStr | None = None


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
