import re
from app.agents.base import BaseAgent
from app.db.models.project import Project
import structlog

logger = structlog.get_logger(__name__)


class TelegramGeneratorAgent(BaseAgent):
    """Генерирует Telegram-бота на aiogram."""

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
Generate a complete Telegram bot using aiogram 3.x, Python 3.12 for:
{query}

Include:
- main.py with bot and dispatcher setup
- handlers/ package with at least start, help commands
- state machine (FSM) if needed
- database integration (SQLAlchemy async + PostgreSQL or SQLite) if needed
- Dockerfile, docker-compose.yml
- requirements.txt, .env.example
- pytest configuration with basic tests (mocked bot)

Provide each file in the format:
---FILE: path/to/file.py---
```python
... code ...
"""

def _parse_files(self, text: str) -> dict[str, str]:
pattern = r'---FILE:\s(.+?)---\s(?:python)?\n(.*?)'
matches = re.findall(pattern, text, re.DOTALL)
return {path.strip(): code.strip() for path, code in matches}
