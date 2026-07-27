from uuid import UUID
from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.services.agent_orchestrator import AgentOrchestrator
import asyncio


@celery_app.task
def run_generation_pipeline(project_id: str):
    async def _run():
        async with AsyncSessionLocal() as session:
            orch = AgentOrchestrator(session, UUID(project_id))
            await orch.run_pipeline()

    asyncio.run(_run())
