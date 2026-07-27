from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    async def execute(self) -> None:
        from app.db.models.project import Project

        project = await self.session.get(Project, self.project_id)
        prompt = f"""
You are a senior software architect. Plan a complete project structure for the following request:
Query: {project.natural_language_query}
Target type: {project.target_type}

Provide:
1. High-level architecture (Clean Architecture, DDD, SOLID).
2. Component list: backend, frontend, database, Docker, CI/CD, tests, docs.
3. Directory tree.
4. Technology stack details.
5. Data model outline.
Return a structured JSON.
"""
        plan = await self.llm.generate(prompt)
        await self._save_artifact("PLAN.md", plan, self.task_id)
