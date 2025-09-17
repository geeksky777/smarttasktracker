from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user as user_service


router = APIRouter(prefix="/user", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    Возвращает UserRead.
    """
    return await user_service.create_user(user_data=user_data, session=session)


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    await user_service.delete_user(current_user, session)


@router.patch("/update", response_model=UserRead)
async def update_user(
    new_user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await user_service.update_user(
        current_user=current_user,
        session=session,
        new_user_data=new_user_data,
    )
