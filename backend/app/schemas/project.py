from uuid import UUID
from datetime import datetime
from pydantic import Field
from app.schemas.common import BaseSchema, PaginatedResponse


class ProjectCreateRequest(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    natural_language_query: str = Field(min_length=10)
    target_type: str  # fastapi, django, telegram_bot, discord_bot, cli, desktop, rest_api, microservice


class ProjectResponse(BaseSchema):
    id: UUID
    name: str
    description: str | None
    natural_language_query: str
    target_type: str
    status: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime | None


class ProjectListResponse(PaginatedResponse):
    items: list[ProjectResponse]