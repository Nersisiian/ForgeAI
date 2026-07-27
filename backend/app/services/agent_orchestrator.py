from uuid import UUID
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.project import Project
from app.db.models.generation_task import GenerationTask
from app.agents.planner import PlannerAgent
from app.agents.architect import ArchitectAgent
from app.agents.backend_generator import BackendGeneratorAgent
from app.agents.frontend_generator import FrontendGeneratorAgent
from app.agents.database_generator import DatabaseGeneratorAgent
from app.agents.docker_generator import DockerGeneratorAgent
from app.agents.testing_generator import TestingGeneratorAgent
from app.agents.documentation_generator import DocumentationGeneratorAgent
from app.agents.review_agent import ReviewAgent
from app.agents.fix_agent import FixAgent
import structlog

logger = structlog.get_logger(__name__)

AGENT_MAP = {
    "planner": PlannerAgent,
    "architect": ArchitectAgent,
    "backend": BackendGeneratorAgent,
    "frontend": FrontendGeneratorAgent,
    "database": DatabaseGeneratorAgent,
    "docker": DockerGeneratorAgent,
    "testing": TestingGeneratorAgent,
    "documentation": DocumentationGeneratorAgent,
    "review": ReviewAgent,
    "fix": FixAgent,
}


class AgentOrchestrator:
    """Orchestrates the multi-agent generation pipeline for a project."""

    def __init__(self, session: AsyncSession, project_id: UUID):
        self.session = session
        self.project_id = project_id

    async def run_pipeline(self):
        project = await self.session.get(Project, self.project_id)
        if not project:
            logger.error("Project not found", project_id=self.project_id)
            return

        # Pipeline order: planner -> architect -> database -> backend -> frontend -> docker -> testing -> documentation -> review -> fix
        pipeline = ["planner", "architect", "database", "backend", "frontend", "docker", "testing", "documentation"]
        for agent_type in pipeline:
            task = GenerationTask(
                project_id=self.project_id,
                agent_type=agent_type,
                status="queued",
                input_data={"project_query": project.natural_language_query, "target_type": project.target_type},
            )
            self.session.add(task)
            await self.session.commit()
            await self.session.refresh(task)

            agent_class = AGENT_MAP[agent_type]
            agent = agent_class(self.session, task.id, self.project_id)
            try:
                task.status = "running"
                await self.session.commit()
                await agent.execute()
                task.status = "success"
                task.completed_at = func.now()
            except Exception as e:
                logger.error("Agent failed", agent=agent_type, error=str(e))
                task.status = "failed"
                task.error_message = str(e)
                await self.session.commit()
                break
            await self.session.commit()

        # Run review and fix loop
        await self._review_and_fix(project)

    async def _review_and_fix(self, project: Project):
        review_task = GenerationTask(project_id=project.id, agent_type="review", status="queued")
        self.session.add(review_task)
        await self.session.commit()
        await self.session.refresh(review_task)
        review_agent = ReviewAgent(self.session, review_task.id, project.id)
        try:
            review_task.status = "running"
            await self.session.commit()
            issues = await review_agent.review()
            review_task.status = "success"
            review_task.output_data = {"issues": issues}
            await self.session.commit()
        except Exception as e:
            review_task.status = "failed"
            review_task.error_message = str(e)
            await self.session.commit()
            return

        if issues:
            fix_task = GenerationTask(project_id=project.id, agent_type="fix", status="queued",
                                       input_data={"issues": issues})
            self.session.add(fix_task)
            await self.session.commit()
            await self.session.refresh(fix_task)
            fix_agent = FixAgent(self.session, fix_task.id, project.id)
            try:
                fix_task.status = "running"
                await self.session.commit()
                await fix_agent.fix(issues)
                fix_task.status = "success"
                await self.session.commit()
            except Exception as e:
                fix_task.status = "failed"
                fix_task.error_message = str(e)
                await self.session.commit()
