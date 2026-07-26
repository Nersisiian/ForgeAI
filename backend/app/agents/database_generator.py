from app.agents.base import BaseAgent
import re


class DatabaseGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        prompt = "Generate complete database schema (SQLAlchemy models + Alembic migration) based on architecture spec."
        response = await self.llm.generate(prompt)
        files = self._parse_files(response)
        for fpath, content in files.items():
            await self._save_artifact(fpath, content, self.task_id)

    def _parse_files(self, text: str) -> dict[str, str]:
        pattern = r'---FILE:\s*(.+?)---\s*```(?:python)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return {path.strip(): code.strip() for path, code in matches}