from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr
from typing import Annotated


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  # user_id
    username: str | None = None
    type: str | None = None  # "access", "refresh"


class UserLogin(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(50)] | None
    email: EmailStr | None
    password: Annotated[str, MinLen(8), MaxLen(50)]
