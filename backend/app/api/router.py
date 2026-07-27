from fastapi import APIRouter
from app.api.v1 import (
    auth,
    projects,
    tasks,
    agents,
    artifacts,
    users,
    settings,
    websocket,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/v1")
api_router.include_router(projects.router, prefix="/v1")
api_router.include_router(tasks.router, prefix="/v1")
api_router.include_router(agents.router, prefix="/v1")
api_router.include_router(artifacts.router, prefix="/v1")
api_router.include_router(users.router, prefix="/v1")
api_router.include_router(settings.router, prefix="/v1")
api_router.include_router(websocket.router, prefix="/v1")
