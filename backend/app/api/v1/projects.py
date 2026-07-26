from uuid import UUID
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_active_user
from app.db.models.user import User
from app.schemas.project import ProjectCreateRequest, ProjectResponse, ProjectListResponse
from app.services.project_service import ProjectService
from app.services.agent_orchestrator import AgentOrchestrator

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    data: ProjectCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = ProjectService(db)
    project = await service.create_project(data, current_user.id)
    orchestrator = AgentOrchestrator(db, project.id)
    background_tasks.add_task(orchestrator.run_pipeline)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = ProjectService(db)
    return await service.get_project(project_id, current_user.id)


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    service = ProjectService(db)
    return await service.list_projects(current_user.id, page, page_size)