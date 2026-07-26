from app.agents.base import BaseAgent


class DocumentationGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        prompt = "Generate README.md, API docs, Architecture guide, Deployment guide for the project."
        response = await self.llm.generate(prompt)
        await self._save_artifact("README.md", response, self.task_id)