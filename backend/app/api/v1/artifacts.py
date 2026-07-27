from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_active_user
from app.db.models.file_artifact import FileArtifact
from app.db.models.project import Project
from app.schemas.artifact import ArtifactResponse, ArtifactUpdateRequest

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.get("/project/{project_id}", response_model=list[ArtifactResponse])
async def get_artifacts(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    project = await db.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403)
    artifacts = (
        (
            await db.execute(
                select(FileArtifact).where(FileArtifact.project_id == project_id)
            )
        )
        .scalars()
        .all()
    )
    return [ArtifactResponse.model_validate(a) for a in artifacts]


@router.put("/{artifact_id}", response_model=ArtifactResponse)
async def update_artifact(
    artifact_id: UUID,
    data: ArtifactUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    artifact = await db.get(FileArtifact, artifact_id)
    if not artifact:
        raise HTTPException(status_code=404)
    project = await db.get(Project, artifact.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(artifact, key, value)
    await db.commit()
    await db.refresh(artifact)
    return ArtifactResponse.model_validate(artifact)
