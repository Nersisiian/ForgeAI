import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class GenerationTask(Base, TimestampMixin):
    __tablename__ = "generation_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    agent_type = Column(String(50), nullable=False)  # planner, architect, backend, etc.
    status = Column(String(50), default="queued")  # queued, running, success, failed
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="tasks")
    agent_runs = relationship(
        "AgentRun", back_populates="task", order_by="AgentRun.created_at"
    )
    artifacts = relationship("FileArtifact", back_populates="task")
