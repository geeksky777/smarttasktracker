import datetime
from sqlalchemy import DateTime, Enum, String, Text, ForeignKey, UniqueConstraint
from app.db.base import Base
from app.db.mixins import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.enums import Status


class Task(Base, TimeStampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="status_enum"),
        default=Status.not_completed,
    )
    completed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="tasks")
    subtasks = relationship(
        "SubTask",
        back_populates="task",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "order_number", name="uq_task_serial"),
    )
