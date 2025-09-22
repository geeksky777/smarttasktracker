from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth_dependency import get_current_user
from app.dependencies.task_dependency import get_task_by_order_number
from app.models.task import Task
from app.services import task as task_service
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/task", tags=["Task"])


@router.get("/all", response_model=list[TaskRead])
async def get_tasks(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.get_tasks(session, current_user)


@router.get("/{order_number}", response_model=TaskRead)
async def get_task(task: Task = Depends(get_task_by_order_number)):
    return task


@router.post("/create", response_model=TaskRead)
async def create_task(
    task_in: TaskCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.create_task(
        session=session, current_user=current_user, task_in=task_in
    )


@router.delete("/delete/{order_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task: Task = Depends(get_task_by_order_number),
    session: AsyncSession = Depends(get_db),
):
    await task_service.delete_task(
        session=session,
        task=task,
    )


@router.patch("/update/{order_number}", response_model=TaskRead)
async def update_user(
    new_task_data: TaskUpdate,
    task: Task = Depends(get_task_by_order_number),
    session: AsyncSession = Depends(get_db),
):
    return await task_service.update_task(
        session=session,
        task=task,
        new_task_data=new_task_data,
    )
