from app.agents.base import BaseAgent
from app.db.models.file_artifact import FileArtifact
from sqlalchemy import select


class ReviewAgent(BaseAgent):
    async def execute(self) -> None:
        await self.review()

    async def review(self) -> list[dict]:
        artifacts = (await self.session.execute(
            select(FileArtifact).where(FileArtifact.project_id == self.project_id)
        )).scalars().all()
        issues = []
        for art in artifacts:
            if art.file_path.endswith('.py'):
                valid, errors = await self.validator.lint_code(art.file_path, art.content)
                if not valid:
                    issues.append({"file": art.file_path, "errors": errors})
                # also check type hints? optional
        return issues