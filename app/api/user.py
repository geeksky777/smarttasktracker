from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User
from app.schemas.auth import UserRead

router = APIRouter(prefix="/user", tags=["Auth"])


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
