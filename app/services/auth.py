from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.auth import UserCreate, Token
from app.core.security import verify_password, create_access_token, create_refresh_token


async def register_user(user_data: UserCreate, session: AsyncSession) -> User:
    repo = UserRepository(session)

    existing_username = await repo.get_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    existing_email = await repo.get_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    user = await repo.create(user_data)

    return user


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


# Авторизация без Ouath2, просто через тело и получение в ответ токенов
# async def authenticate_user(login_data: UserLogin, session: AsyncSession) -> Token:
#     repo = UserRepository(session)

#     login = login_data.username or login_data.email
#     if not login:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username or Email required,",
#         )

#     user = await repo.get_by_login(login)
#     if not user or not verify_password(login_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid login or password",
#         )
#     access = create_access_token({"sub": str(user.id), "username": user.username})
#     refresh = create_refresh_token({"sub": str(user.id), "username": user.username})
#     return Token(access_token=access, refresh_token=refresh)
