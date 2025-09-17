from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.repositories.user_repo import UserRepository
from app.schemas.auth import Token
from app.core.security import verify_password, create_access_token, create_refresh_token


async def authenticate_user_oauth(
    form_data: OAuth2PasswordRequestForm,
    session: AsyncSession,
) -> Token:
    repo = UserRepository(session)
    user = await repo.get_by_login(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password",
        )

    access = create_access_token({"sub": str(user.id), "username": user.username})
    refresh = create_refresh_token({"sub": str(user.id), "username": user.username})
    return Token(access_token=access, refresh_token=refresh)
