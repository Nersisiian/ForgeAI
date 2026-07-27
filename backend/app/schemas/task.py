from uuid import UUID
from datetime import datetime
from app.schemas.common import BaseSchema


class TaskResponse(BaseSchema):
    id: UUID
    project_id: UUID
    agent_type: str
    status: str
    input_data: dict | None
    output_data: dict | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
