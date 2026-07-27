from app.agents.base import BaseAgent


class ArchitectAgent(BaseAgent):
    async def execute(self) -> None:
        from app.db.models.project import Project

        project = await self.session.get(Project, self.project_id)
        prompt = f"""
Based on this plan, produce a detailed technical specification:
Plan: (from previous artifact)

Target: {project.target_type}
Query: {project.natural_language_query}

Output:
- Database schema (tables, columns, types, constraints)
- API endpoints (REST/GraphQL)
- Frontend component tree
- Security model
- Deployment architecture
Return a detailed Markdown spec.
"""
        # In a full implementation we would read the plan artifact.
        spec = await self.llm.generate(prompt)
        await self._save_artifact("ARCHITECTURE.md", spec, self.task_id)
