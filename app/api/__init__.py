from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.task import router as task_router

routers = [
    auth_router,
    user_router,
    task_router,
]
