from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.llm_service import LLMService
from app.services.validation_service import ValidationService
import structlog

logger = structlog.get_logger(__name__)


class BaseAgent(ABC):
    """Abstract base for all generation agents."""

    def __init__(self, session: AsyncSession, task_id: UUID, project_id: UUID):
        self.session = session
        self.task_id = task_id
        self.project_id = project_id
        self.llm = LLMService()
        self.validator = ValidationService()

    @abstractmethod
    async def execute(self) -> None:
        """Run the agent's generation logic."""
        ...

    async def _save_artifact(
        self, file_path: str, content: str, task_id: UUID | None = None
    ) -> None:
        from app.db.models.file_artifact import FileArtifact

        artifact = FileArtifact(
            project_id=self.project_id,
            task_id=task_id or self.task_id,
            file_path=file_path,
            content=content,
            status="draft",
        )
        self.session.add(artifact)
        await self.session.commit()

    async def _validate_and_fix(
        self, file_path: str, content: str, task_id: UUID
    ) -> str:
        """Validate file, if issues found attempt auto-fix via LLM."""
        valid, errors = await self.validator.lint_code(file_path, content)
        if not valid:
            logger.warning(
                "Lint errors found, attempting fix", file=file_path, errors=errors
            )
            fix_prompt = (
                f"The following code has lint errors:\n```python\n{content}\n```\n"
                f"Errors:\n{chr(10).join(errors)}\n"
                "Fix the code and return only the corrected Python code, no explanations."
            )
            fixed = await self.llm.generate(fix_prompt)
            # re-validate
            valid2, _ = await self.validator.lint_code(file_path, fixed)
            if valid2:
                return fixed
            else:
                logger.error("Auto-fix failed for", file=file_path)
        return content
