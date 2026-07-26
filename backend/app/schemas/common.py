from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseSchema):
    items: list
    total: int
    page: int
    page_size: int


class MessageResponse(BaseSchema):
    message: str