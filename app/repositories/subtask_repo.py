from sqlite3 import IntegrityError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User
from app.models.subtask import SubTask
from app.schemas.subtask import SubTaskCreate, SubTaskUpdate


class SubTaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_next_order_number(self, task: Task) -> int:
        q = select(func.max(SubTask.order_number)).where(SubTask.task_id == task.id)
        result = await self.session.execute(q)
        max_order = result.scalar() or 0
        return max_order + 1

    async def create(
        self,
        task: Task,
        subtask_in: SubTaskCreate,
    ) -> SubTask:
        subtask_data = subtask_in.model_dump(exclude_unset=True)

        next_order = await self._get_next_order_number(task)

        if "order_number" not in subtask_data:
            subtask_data["order_number"] = next_order
        else:
            q = select(SubTask.id).where(
                SubTask.task_id == task.id,
                SubTask.order_number == subtask_data["order_number"],
            )
            exists = await self.session.execute(q)
            if exists.scalar() is not None:
                subtask_data["order_number"] = next_order

        subtask = SubTask(**subtask_data, task_id=task.id)
        self.session.add(subtask)
        await self.session.commit()
        await self.session.refresh(subtask)
        return subtask

    async def get_subtasks(self, task: Task) -> list[SubTask]:
        q = (
            select(SubTask)
            .where(SubTask.task_id == task.id)
            .order_by(SubTask.order_number)
        )
        result = await self.session.scalars(q)
        return result.all()

    async def update():
        pass

    async def delete(self, subtask: SubTask) -> None:
        await self.session.delete(subtask)
        await self.session.commit()

    async def get_subtask_by_order_number(
        self,
        task: Task,
        subtask_order_number: int,
    ) -> SubTask | None:
        q = select(SubTask).where(
            SubTask.task_id == task.id,
            SubTask.order_number == subtask_order_number,
        )
        result = await self.session.execute(q)
        return result.scalar_one_or_none()

    async def update(
        self, subtask: SubTask, new_subtask_data: SubTaskUpdate
    ) -> SubTask | bool:
        to_update = new_subtask_data.model_dump(exclude_unset=True)
        if not to_update:
            return subtask
        if "order_number" in to_update:
            new_order = to_update["order_number"]

            if new_order == subtask.order_number:
                to_update.pop("order_number")
            else:
                # проверяем, не занят ли новый номер другой задачей пользователя
                stmt = select(SubTask.id).where(
                    SubTask.task_id == subtask.task_id,
                    SubTask.order_number == new_order,
                    SubTask.id != subtask.id,
                )
                result = await self.session.execute(stmt)
                if result.scalar_one_or_none() is not None:
                    return False
        for field, value in to_update.items():
            if hasattr(subtask, field):
                setattr(subtask, field, value)
        try:
            self.session.add(subtask)
            await self.session.commit()
            await self.session.refresh(subtask)
            return subtask
        except IntegrityError:
            await self.session.rollback()
            return False
