from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.models.task import Task
from app.models.user import User
from app.repositories.task_repo import TaskRepository


async def get_task_by_order_number(
    order_number: Annotated[int, Path(..., ge=1)],
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    repo = TaskRepository(session)
    task = await repo.get_task_by_order_number(order_number, current_user)
    if task:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )
