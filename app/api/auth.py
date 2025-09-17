from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import UserCreate, Token, UserRead
from app.db.session import get_db
from app.services.auth import register_user, authenticate_user_oauth

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    Возвращает UserRead.
    """
    return await register_user(user_data=user_data, session=session)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    return await authenticate_user_oauth(form_data=form_data, session=session)
