from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.exceptions import NotFoundError, ForbiddenError
from app.db.models.project import Project
from app.db.models.file_artifact import FileArtifact
from app.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectListResponse,
)


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_project(
        self, data: ProjectCreateRequest, owner_id: UUID
    ) -> ProjectResponse:
        project = Project(
            **data.model_dump(),
            owner_id=owner_id,
        )
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return ProjectResponse.model_validate(project)

    async def get_project(self, project_id: UUID, user_id: UUID) -> ProjectResponse:
        project = await self.session.get(Project, project_id)
        if not project:
            raise NotFoundError("Project not found")
        if project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        return ProjectResponse.model_validate(project)

    async def list_projects(
        self, user_id: UUID, page: int = 1, page_size: int = 20
    ) -> ProjectListResponse:
        query = (
            select(Project)
            .where(Project.owner_id == user_id)
            .order_by(Project.created_at.desc())
        )
        count_query = (
            select(func.count()).select_from(Project).where(Project.owner_id == user_id)
        )
        total = (await self.session.execute(count_query)).scalar()
        projects = (
            (
                await self.session.execute(
                    query.offset((page - 1) * page_size).limit(page_size)
                )
            )
            .scalars()
            .all()
        )
        return ProjectListResponse(
            items=[ProjectResponse.model_validate(p) for p in projects],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_artifacts(self, project_id: UUID, user_id: UUID) -> list:
        project = await self.session.get(Project, project_id)
        if not project or project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        artifacts = (
            (
                await self.session.execute(
                    select(FileArtifact).where(FileArtifact.project_id == project_id)
                )
            )
            .scalars()
            .all()
        )
        return artifacts
