from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_active_user
from app.db.models.generation_task import GenerationTask
from app.db.models.project import Project
from app.schemas.task import TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/project/{project_id}", response_model=list[TaskResponse])
async def get_project_tasks(
project_id: UUID,
db: AsyncSession = Depends(get_db),
current_user=Depends(get_current_active_user),
):
project = await db.get(Project, project_id)
if not project or project.owner_id != current_user.id:
raise HTTPException(status_code=403)
tasks = (await db.execute(
select(GenerationTask).where(GenerationTask.project_id == project_id).order_by(GenerationTask.created_at)
)).scalars().all()
return [TaskResponse.model_validate(t) for t in tasks]
