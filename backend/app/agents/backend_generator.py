from app.agents.base import BaseAgent
import json
import re


class BackendGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        from app.db.models.project import Project
        project = await self.session.get(Project, self.project_id)

        # Generate main application structure
        prompt = f"""
Generate a complete FastAPI backend for: {project.natural_language_query}
Target type: {project.target_type}
Follow Clean Architecture, DDD, SOLID.
Use SQLAlchemy 2.0 async, Alembic, JWT auth, role-based permissions, WebSockets, background tasks.
Provide each file in the format:
---FILE: path/to/file.py---
```python
... code ...
Include: main.py, config.py, database.py, models, schemas, api routes, services, dependencies, middleware, Dockerfile, requirements.txt.
"""
response = await self.llm.generate(prompt)
files = self._parse_files(response)
for fpath, content in files.items():
validated = await self._validate_and_fix(fpath, content, self.task_id)
await self._save_artifact(fpath, validated, self.task_id)

def _parse_files(self, text: str) -> dict[str, str]:
pattern = r'---FILE:\s(.+?)---\s(?:python)?\n(.*?)'
matches = re.findall(pattern, text, re.DOTALL)
return {path.strip(): code.strip() for path, code in matches}

#### `backend/app/agents/frontend_generator.py`
```python
from app.agents.base import BaseAgent
import re


class FrontendGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        from app.db.models.project import Project
        project = await self.session.get(Project, self.project_id)
        prompt = f"""
Generate a React TypeScript frontend for: {project.natural_language_query}
Use Vite, Material UI, Dark Mode, React Router, Axios.
Include: main.tsx, App.tsx, components, pages, hooks, services, theme, package.json, tsconfig.json, vite.config.ts, Dockerfile.
Output each file with ---FILE: path--- marker.
"""
        response = await self.llm.generate(prompt)
        files = self._parse_files(response)
        for fpath, content in files.items():
            await self._save_artifact(fpath, content, self.task_id)

    def _parse_files(self, text: str) -> dict[str, str]:
        pattern = r'---FILE:\s*(.+?)---\s*```(?:tsx|ts|json)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return {path.strip(): code.strip() for path, code in matches}