import re
from app.agents.base import BaseAgent
from app.db.models.project import Project
import structlog

logger = structlog.get_logger(__name__)


class DjangoGeneratorAgent(BaseAgent):
    """Генерирует полный проект Django (модели, админка, DRF, настройки)."""

    async def execute(self) -> None:
        project = await self.session.get(Project, self.project_id)
        if not project:
            logger.error("Project not found", project_id=self.project_id)
            return

        prompt = self._build_prompt(project.natural_language_query)
        response = await self.llm.generate(prompt)
        files = self._parse_files(response)
        for fpath, content in files.items():
            validated = await self._validate_and_fix(fpath, content, self.task_id)
            await self._save_artifact(fpath, validated, self.task_id)

    def _build_prompt(self, query: str) -> str:
        return f"""
Generate a complete Django project (Python 3.12, Django 5.0, Django REST Framework) for the following requirement:
{query}

Include:
- Project layout with manage.py, settings.py (split for dev/prod), urls.py, wsgi.py, asgi.py
- At least one Django app (e.g., core or main)
- Models with fields, relationships, indexes
- Admin configuration
- DRF serializers, views, routers
- JWT authentication (djangorestframework-simplejwt)
- Dockerfile, docker-compose with PostgreSQL, Redis, Celery (optional)
- pytest configuration, factories (factory_boy), basic tests
- requirements.txt

Provide each file in the format:
---FILE: path/to/file.py---
```python
... code ...
"""

def _parse_files(self, text: str) -> dict[str, str]:
pattern = r'---FILE:\s(.+?)---\s(?:python)?\n(.*?)'
matches = re.findall(pattern, text, re.DOTALL)
return {path.strip(): code.strip() for path, code in matches}
