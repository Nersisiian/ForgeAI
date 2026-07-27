from uuid import UUID
from datetime import datetime
from app.schemas.common import BaseSchema


class ArtifactResponse(BaseSchema):
    id: UUID
    project_id: UUID
    task_id: UUID | None
    file_path: str
    content: str | None
    status: str
    review_comment: str | None
    created_at: datetime
    updated_at: datetime | None


class ArtifactUpdateRequest(BaseSchema):
    content: str | None = None
    review_comment: str | None = None
    status: str | None = None
