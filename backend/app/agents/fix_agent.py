from app.agents.base import BaseAgent
from app.db.models.file_artifact import FileArtifact
from sqlalchemy import select


class FixAgent(BaseAgent):
    async def execute(self) -> None:
        issues = self.task.input_data.get("issues", [])
        await self.fix(issues)

    async def fix(self, issues: list[dict]) -> None:
        for issue in issues:
            file_path = issue["file"]
            artifact = (
                await self.session.execute(
                    select(FileArtifact).where(
                        FileArtifact.project_id == self.project_id,
                        FileArtifact.file_path == file_path,
                    )
                )
            ).scalar_one_or_none()
            if artifact:
                fix_prompt = (
                    f"Fix the following Python code to resolve these lint errors:\n"
                    f"Code:\n```python\n{artifact.content}\n```\n"
                    f"Errors:\n{issue['errors']}\n"
                    f"Return only the fixed Python code."
                )
                fixed = await self.llm.generate(fix_prompt)
                valid, _ = await self.validator.lint_code(file_path, fixed)
                if valid:
                    artifact.content = fixed
                    artifact.status = "approved"
                    await self.session.commit()
