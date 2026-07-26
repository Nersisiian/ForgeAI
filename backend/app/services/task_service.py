from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.generation_task import GenerationTask
from app.db.models.project import Project
from app.core.exceptions import NotFoundError, ForbiddenError
from app.schemas.task import TaskResponse
import structlog

logger = structlog.get_logger(__name__)


class TaskService:
    """Service for managing generation tasks."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks_for_project(self, project_id: UUID, user_id: UUID) -> List[TaskResponse]:
        project = await self.session.get(Project, project_id)
        if not project:
            raise NotFoundError("Project not found")
        if project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        query = select(GenerationTask).where(
            GenerationTask.project_id == project_id
        ).order_by(GenerationTask.created_at)
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return [TaskResponse.model_validate(t) for t in tasks]

    async def get_task(self, task_id: UUID, user_id: UUID) -> TaskResponse:
        task = await self.session.get(GenerationTask, task_id)
        if not task:
            raise NotFoundError("Task not found")
        project = await self.session.get(Project, task.project_id)
        if not project or project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        return TaskResponse.model_validate(task)

    async def update_task_status(
        self, task_id: UUID, status: str, error_message: Optional[str] = None
    ) -> TaskResponse:
        task = await self.session.get(GenerationTask, task_id)
        if not task:
            raise NotFoundError("Task not found")
        task.status = status
        if error_message:
            task.error_message = error_message
        await self.session.commit()
        await self.session.refresh(task)
        return TaskResponse.model_validate(task)

    async def create_task(
        self, project_id: UUID, agent_type: str, input_data: Optional[dict] = None
    ) -> TaskResponse:
        task = GenerationTask(
            project_id=project_id,
            agent_type=agent_type,
            status="queued",
            input_data=input_data or {},
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return TaskResponse.model_validate(task)