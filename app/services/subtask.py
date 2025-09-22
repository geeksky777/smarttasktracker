from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.subtask import SubTask
from app.models.task import Task
from app.repositories.subtask_repo import SubTaskRepository
from app.schemas.subtask import SubTaskCreate, SubTaskUpdate


async def create_subtask(
    session: AsyncSession, task: Task, subtask_in: SubTaskCreate
) -> SubTask:
    repo = SubTaskRepository(session)
    return await repo.create(task, subtask_in)


async def read_subtasks(session: AsyncSession, task: Task) -> list[SubTask]:
    repo = SubTaskRepository(session)
    return await repo.get_subtasks(task)


async def delete_subtask(session: AsyncSession, subtask: SubTask) -> None:
    repo = SubTaskRepository(session)
    await repo.delete(subtask)


async def update_subtask(
    session: AsyncSession,
    subtask: SubTask,
    new_subtask_data: SubTaskUpdate,
) -> SubTask:
    repo = SubTaskRepository(session)
    updated = await repo.update(subtask, new_subtask_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Order number already exists"
        )
    return updated
