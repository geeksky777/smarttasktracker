from sqlalchemy import String
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.mixins import TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
