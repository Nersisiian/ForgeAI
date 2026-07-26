from app.agents.base import BaseAgent


class TestingGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        prompt = "Generate comprehensive pytest tests (unit, integration) for the project with >90% coverage."
        response = await self.llm.generate(prompt)
        await self._save_artifact("tests/test_main.py", response, self.task_id)