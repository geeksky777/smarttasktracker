from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.subtask_dependecy import get_subtask_by_order_number
from app.dependencies.task_dependency import get_task_by_order_number
from app.models.subtask import SubTask
from app.services import subtask as subtask_service
from app.models.task import Task
from app.schemas.subtask import SubTaskCreate, SubTaskRead, SubTaskUpdate

router = APIRouter(prefix="/task/{order_number}", tags=["SubTask"])


@router.post("/create", response_model=SubTaskRead)
async def create_subtask(
    subtask_in: SubTaskCreate,
    session: AsyncSession = Depends(get_db),
    task: Task = Depends(get_task_by_order_number),
):
    return await subtask_service.create_subtask(session, task, subtask_in)


@router.get("/subtasks", response_model=list[SubTaskRead])
async def get_subtasks(
    session: AsyncSession = Depends(get_db),
    task: Task = Depends(get_task_by_order_number),
):
    return await subtask_service.read_subtasks(session, task)


@router.get("/{subtask_order_number}", response_model=SubTaskRead)
async def get_subtask(
    subtask: SubTask = Depends(get_subtask_by_order_number),
):
    return subtask


@router.delete("/delete/{subtask_order_number}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subtask(
    subtask: SubTask = Depends(get_subtask_by_order_number),
    session: AsyncSession = Depends(get_db),
):
    await subtask_service.delete_subtask(session, subtask)


@router.patch("/update/{subtask_order_number}", response_model=SubTaskRead)
async def update_subtask(
    new_subtask_data: SubTaskUpdate,
    subtask: SubTask = Depends(get_subtask_by_order_number),
    session: AsyncSession = Depends(get_db),
):
    return await subtask_service.update_subtask(session, subtask, new_subtask_data)
