from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
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


async def delete_user(current_user: User, session: AsyncSession) -> None:
    repo = UserRepository(session)
    await repo.delete(current_user)


async def update_user(
    current_user: User,
    session: AsyncSession,
    new_user_data: UserUpdate,
) -> User:
    repo = UserRepository(session)
    return await repo.update(current_user=current_user, new_user_data=new_user_data)
