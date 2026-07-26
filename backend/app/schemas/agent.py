from uuid import UUID
from datetime import datetime
from app.schemas.common import BaseSchema


class AgentRunResponse(BaseSchema):
    id: UUID
    task_id: UUID
    agent_name: str
    prompt: str | None
    response: str | None
    status: str
    created_at: datetime
    completed_at: datetime | None