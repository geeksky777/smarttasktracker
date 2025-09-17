from app.api.auth import router as auth_router
from app.api.user import router as user_router

routers = [
    auth_router,
    user_router,
]
