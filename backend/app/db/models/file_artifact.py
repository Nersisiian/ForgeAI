import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class FileArtifact(Base, TimestampMixin):
    __tablename__ = "file_artifacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    task_id = Column(
        UUID(as_uuid=True), ForeignKey("generation_tasks.id"), nullable=True
    )
    file_path = Column(String(500), nullable=False)
    content = Column(Text, nullable=True)
    status = Column(String(50), default="draft")  # draft, reviewed, approved, rejected
    review_comment = Column(Text, nullable=True)

    project = relationship("Project", back_populates="artifacts")
    task = relationship("GenerationTask", back_populates="artifacts")
