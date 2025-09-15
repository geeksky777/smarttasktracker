import datetime
from sqlalchemy import DateTime, Enum, String, ForeignKey, UniqueConstraint
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.mixins import TimeStampMixin
from app.db.enums import Status


class SubTask(Base, TimeStampMixin):
    __tablename__ = "subtasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(100))
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="status_enum"),
        default=Status.not_completed,
    )
    completed_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))

    task = relationship("Task", back_populates="subtasks")

    __table_args__ = (
        UniqueConstraint("task_id", "order_number", name="uq_subtask_serial"),
    )
