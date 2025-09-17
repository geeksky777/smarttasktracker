from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Annotated


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  # user_id
    username: str | None = None
    type: str | None = None  # "access", "refresh"


class UserCreate(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(50)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(50)]


class UserLogin(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(50)] | None
    email: EmailStr | None
    password: Annotated[str, MinLen(8), MaxLen(50)]


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
