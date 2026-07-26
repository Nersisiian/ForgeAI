from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.dependencies import get_db, get_current_active_user
from app.db.models.agent_run import AgentRun
from app.schemas.agent import AgentRunResponse

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/task/{task_id}", response_model=list[AgentRunResponse])
async def get_agent_runs(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    runs = (await db.execute(
        select(AgentRun).where(AgentRun.task_id == task_id).order_by(AgentRun.created_at)
    )).scalars().all()
    return [AgentRunResponse.model_validate(r) for r in runs]