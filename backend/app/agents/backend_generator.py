import re
from app.agents.base import BaseAgent
from app.db.models.project import Project
import structlog

logger = structlog.get_logger(__name__)


class BackendGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        project = await self.session.get(Project, self.project_id)
        if not project:
            logger.error("Project not found", project_id=self.project_id)
            return

        prompt = self._build_prompt(project.natural_language_query, project.target_type)
        response = await self.llm.generate(prompt)
        files = self._parse_files(response)
        for fpath, content in files.items():
            validated = await self._validate_and_fix(fpath, content, self.task_id)
            await self._save_artifact(fpath, validated, self.task_id)

    def _build_prompt(self, query: str, target_type: str) -> str:
        return f"""
Generate a complete FastAPI backend for: {query}
Target type: {target_type}
Follow Clean Architecture, DDD, SOLID.
Use SQLAlchemy 2.0 async, Alembic, JWT auth, role-based permissions, WebSockets, background tasks.
Provide each file in the format:
---FILE: path/to/file.py---
```python
... code ...
Include: main.py, config.py, database.py, models, schemas, api routes, services, dependencies, middleware, Dockerfile, requirements.txt.
"""
    def _parse_files(self, text: str) -> dict[str, str]:
        pattern = r"---FILE:\s(.+?)---\s(?:```python\n)?(.*?)```?" 
        matches = re.findall(pattern, text, re.DOTALL)
        return {path.strip(): code.strip() for path, code in matches}