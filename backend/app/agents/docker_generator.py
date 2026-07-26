from app.agents.base import BaseAgent


class DockerGeneratorAgent(BaseAgent):
    async def execute(self) -> None:
        prompt = "Generate Dockerfile, docker-compose.yml, and Nginx config for the project."
        response = await self.llm.generate(prompt)
        # simple: save the whole response as docker guide and config files
        await self._save_artifact("Dockerfile", response, self.task_id)  # will be refined