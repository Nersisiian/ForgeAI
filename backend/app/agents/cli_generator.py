import re
from app.agents.base import BaseAgent
from app.db.models.project import Project
import structlog

logger = structlog.get_logger(__name__)


class CLIGeneratorAgent(BaseAgent):
    """Генерирует CLI-утилиту на Click или Typer."""

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
Generate a Python CLI tool using Click (or Typer) for:
{query}

Include:
- main.py with CLI entry point
- commands/ package with subcommands
- setup.py or pyproject.toml for packaging
- Dockerfile (optional)
- requirements.txt, README.md
- pytest configuration with basic tests

Provide each file in the format:
---FILE: path/to/file.py---
`python
... code ...
"""

    def _parse_files(self, text: str) -> dict[str, str]:
        pattern = r"---FILE:\s*(.+?)---\s*`(?:python)?\n(.*?)`"
        matches = re.findall(pattern, text, re.DOTALL)
        return {path.strip(): code.strip() for path, code in matches}
