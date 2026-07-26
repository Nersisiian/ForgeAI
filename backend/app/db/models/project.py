import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    natural_language_query = Column(Text, nullable=False)
    target_type = Column(String(50), nullable=False)  # fastapi, django, telegram_bot, etc.
    status = Column(String(50), default="pending")  # pending, generating, completed, failed
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="projects")
    tasks = relationship("GenerationTask", back_populates="project", order_by="GenerationTask.created_at")
    artifacts = relationship("FileArtifact", back_populates="project", lazy="dynamic")