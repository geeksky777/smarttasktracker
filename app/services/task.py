from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.user import UserUpdate


async def get_tasks(session: AsyncSession, current_user: User) -> list[Task]:
    repo = TaskRepository(session)
    return await repo.read_tasks(current_user)


async def create_task(
    session: AsyncSession, current_user: User, task_in: TaskCreate
) -> User:
    repo = TaskRepository(session)
    return await repo.create(current_user, task_in)


async def delete_task(session: AsyncSession, task: Task) -> None:
    repo = TaskRepository(session)
    await repo.delete(task)


async def update_task(
    session: AsyncSession,
    task: Task,
    new_task_data: TaskUpdate,
) -> Task:
    repo = TaskRepository(session)
    updated = await repo.update(task, new_task_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Order number already exists"
        )
    return updated
