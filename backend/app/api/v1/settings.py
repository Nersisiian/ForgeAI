from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_active_user
from app.core.config import settings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/")
async def get_public_settings(current_user=Depends(get_current_active_user)):
    return {
        "app_name": settings.APP_NAME,
        "llm_model": settings.LLM_MODEL,
    }