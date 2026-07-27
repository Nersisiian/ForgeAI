from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.file_artifact import FileArtifact
from app.db.models.project import Project
from app.core.exceptions import NotFoundError, ForbiddenError
from app.schemas.artifact import ArtifactResponse, ArtifactUpdateRequest
import structlog

logger = structlog.get_logger(__name__)


class ArtifactService:
    """Service for managing generated file artifacts."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_artifacts_for_project(
        self, project_id: UUID, user_id: UUID, file_path_filter: str | None = None
    ) -> List[ArtifactResponse]:
        project = await self.session.get(Project, project_id)
        if not project:
            raise NotFoundError("Project not found")
        if project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        query = select(FileArtifact).where(FileArtifact.project_id == project_id)
        if file_path_filter:
            query = query.where(FileArtifact.file_path.ilike(f"%{file_path_filter}%"))
        query = query.order_by(FileArtifact.file_path)
        result = await self.session.execute(query)
        artifacts = result.scalars().all()
        return [ArtifactResponse.model_validate(a) for a in artifacts]

    async def get_artifact(self, artifact_id: UUID, user_id: UUID) -> ArtifactResponse:
        artifact = await self.session.get(FileArtifact, artifact_id)
        if not artifact:
            raise NotFoundError("Artifact not found")
        project = await self.session.get(Project, artifact.project_id)
        if not project or project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        return ArtifactResponse.model_validate(artifact)

    async def update_artifact(
        self, artifact_id: UUID, user_id: UUID, data: ArtifactUpdateRequest
    ) -> ArtifactResponse:
        artifact = await self.session.get(FileArtifact, artifact_id)
        if not artifact:
            raise NotFoundError("Artifact not found")
        project = await self.session.get(Project, artifact.project_id)
        if not project or project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        update_dict = data.model_dump(exclude_unset=True)
        if "content" in update_dict:
            artifact.content = update_dict["content"]
        if "review_comment" in update_dict:
            artifact.review_comment = update_dict["review_comment"]
        if "status" in update_dict:
            artifact.status = update_dict["status"]
        await self.session.commit()
        await self.session.refresh(artifact)
        return ArtifactResponse.model_validate(artifact)

    async def create_artifact(
        self, project_id: UUID, file_path: str, content: str, task_id: UUID | None = None
    ) -> ArtifactResponse:
        artifact = FileArtifact(
            project_id=project_id,
            task_id=task_id,
            file_path=file_path,
            content=content,
            status="draft",
        )
        self.session.add(artifact)
        await self.session.commit()
        await self.session.refresh(artifact)
        return ArtifactResponse.model_validate(artifact)

    async def delete_artifact(self, artifact_id: UUID, user_id: UUID) -> None:
        artifact = await self.session.get(FileArtifact, artifact_id)
        if not artifact:
            raise NotFoundError("Artifact not found")
        project = await self.session.get(Project, artifact.project_id)
        if not project or project.owner_id != user_id:
            raise ForbiddenError("Access denied")
        await self.session.delete(artifact)
        await self.session.commit()
