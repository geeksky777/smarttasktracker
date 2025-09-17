from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        q = select(User).where(User.id == user_id)
        result = await self.session.execute(q)
        return result.scalar_one_or_none()

    async def get_by_login(self, login: str) -> User | None:
        """
        Ищем юзера либо по username, либо по email.
        """
        q = select(User).where(or_(User.username == login, User.email == login))
        result = await self.session.execute(q)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> User | None:
        q = select(User).where(User.username == username)
        result = await self.session.execute(q)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        q = select(User).where(User.email == email)
        result = await self.session.execute(q)
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User | None:
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
