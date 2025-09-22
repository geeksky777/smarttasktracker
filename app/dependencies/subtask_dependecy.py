from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.task_dependency import get_task_by_order_number
from app.models.subtask import SubTask
from app.models.task import Task
from app.repositories.subtask_repo import SubTaskRepository


async def get_subtask_by_order_number(
    subtask_order_number: Annotated[int, Path(..., ge=1)],
    session: AsyncSession = Depends(get_db),
    task: Task = Depends(get_task_by_order_number),
) -> SubTask:
    repo = SubTaskRepository(session)
    subtask = await repo.get_subtask_by_order_number(task, subtask_order_number)
    if subtask:
        return subtask
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="SubTask not found",
    )
