from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_next_order_number(self, current_user: User) -> int:
        q = select(func.max(Task.order_number)).where(Task.user_id == current_user.id)
        result = await self.session.execute(q)
        max_order = result.scalar() or 0
        return max_order + 1

    async def create(self, current_user: User, task_in: TaskCreate) -> Task:
        # Берём данные из pydantic
        task_data = task_in.model_dump(exclude_unset=True)

        # Узнаём максимальный order_number
        next_order = await self._get_next_order_number(current_user)

        # Если order_number не передан или занят → берём max+1
        if "order_number" not in task_data:
            task_data["order_number"] = next_order
        else:
            # проверим, занят ли такой номер
            q = select(Task.id).where(
                Task.user_id == current_user.id,
                Task.order_number == task_data["order_number"],
            )
            exists = await self.session.execute(q)
            if exists.scalar() is not None:
                task_data["order_number"] = next_order

        # создаём таску
        task = Task(**task_data, user_id=current_user.id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def read_tasks(self, current_user: User) -> list[Task]:
        q = (
            select(Task)
            .where(Task.user_id == current_user.id)
            .order_by(Task.order_number)
        )
        result = await self.session.scalars(q)
        return result.all()

    async def get_task_by_order_number(
        self,
        order_number: int,
        current_user: User,
    ) -> Task | None:
        q = select(Task).where(
            Task.user_id == current_user.id, Task.order_number == order_number
        )
        result = await self.session.scalars(q)
        return result.first()

    async def delete(self, task: Task) -> bool:
        await self.session.delete(task)
        await self.session.commit()

    async def update(self, task: Task, new_task_data: TaskUpdate) -> Task | bool:
        to_update = new_task_data.model_dump(exclude_unset=True)
        if not to_update:
            return task
        if "order_number" in to_update:
            new_order = to_update["order_number"]

            if new_order == task.order_number:
                to_update.pop("order_number")
            else:
                # проверяем, не занят ли новый номер другой задачей пользователя
                stmt = select(Task.id).where(
                    Task.user_id == task.user_id,
                    Task.order_number == new_order,
                    Task.id != task.id,
                )
                result = await self.session.execute(stmt)
                if result.scalar_one_or_none() is not None:
                    return False
        for field, value in to_update.items():
            if hasattr(task, field):
                setattr(task, field, value)
        try:
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)
            return task
        except IntegrityError:
            await self.session.rollback()
            return False
