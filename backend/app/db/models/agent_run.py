import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class AgentRun(Base, TimestampMixin):
    __tablename__ = "agent_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("generation_tasks.id"), nullable=False)
    agent_name = Column(String(100), nullable=False)
    prompt = Column(Text, nullable=True)
    response = Column(Text, nullable=True)
    status = Column(String(50), default="running")  # running, success, failed
    completed_at = Column(DateTime(timezone=True), nullable=True)

    task = relationship("GenerationTask", back_populates="agent_runs")