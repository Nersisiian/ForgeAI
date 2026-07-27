import re
from app.agents.base import BaseAgent
from app.db.models.project import Project
import structlog

logger = structlog.get_logger(__name__)

VALID_FILE_EXTENSIONS = {".tsx", ".ts", ".jsx", ".js", ".json", ".css", ".html", ".svg"}


class FrontendGeneratorAgent(BaseAgent):
    """Generates a complete React/TypeScript frontend based on project specification."""

    async def execute(self) -> None:
        project = await self.session.get(Project, self.project_id)
        if not project:
            logger.error("Project not found", project_id=self.project_id)
            return

        architecture_spec = await self._get_architecture_spec()
        prompt = self._build_prompt(
            project.natural_language_query, project.target_type, architecture_spec
        )

        logger.info("Generating frontend code", project_id=self.project_id)
        response = await self.llm.generate(
            prompt, system_prompt="You are an expert React developer."
        )

        files = self._parse_files(response)
        if not files:
            logger.warning(
                "No files parsed from LLM response", project_id=self.project_id
            )
            return

        for file_path, content in files.items():
            if not any(file_path.endswith(ext) for ext in VALID_FILE_EXTENSIONS):
                logger.warning("Skipping invalid file type", file_path=file_path)
                continue

            if file_path.endswith((".tsx", ".ts", ".jsx", ".js")):
                validated = await self._validate_and_fix(
                    file_path, content, self.task_id
                )
                content = validated

            await self._save_artifact(file_path, content, self.task_id)
            logger.info("Frontend file generated", file_path=file_path)

    def _build_prompt(
        self, query: str, target_type: str, architecture_spec: str
    ) -> str:
        return f"""
Generate a production-ready React frontend application based on the following specification.

Target type: {target_type}
User request: {query}

Architecture specification:
{architecture_spec if architecture_spec else 'Not available - generate a reasonable default.'}

Requirements:
- Use React 18 with TypeScript, Vite, Material UI (MUI) v5.
- Implement a complete set of pages including authentication (login/register), dashboard, and any features needed for the target type.
- Include proper routing with react-router-dom, protected routes, JWT token handling, and automatic token refresh.
- Implement a dark mode theme toggle, responsive layout.
- Use axios for API calls with interceptors for auth.
- Include a WebSocket hook for real-time updates.
- Generate all source files: main.tsx, App.tsx, components, pages, hooks, services, theme, utils.
- Also provide package.json, tsconfig.json, tsconfig.node.json, vite.config.ts, Dockerfile, .env.example.
- Output each file in the format:
  ---FILE: path/to/file.ext---
  ```language
  file content
Ensure all code is syntactically correct and follows best practices.

No placeholders, no TODOs.
"""


async def _get_architecture_spec(self) -> str:
    from sqlalchemy import select
    from app.db.models.file_artifact import FileArtifact

    query = (
        select(FileArtifact)
        .where(
            FileArtifact.project_id == self.project_id,
            FileArtifact.file_path.ilike("%ARCHITECTURE%"),
        )
        .order_by(FileArtifact.created_at.desc())
        .limit(1)
    )
    result = await self.session.execute(query)
    artifact = result.scalar_one_or_none()
    if artifact and artifact.content:
        return artifact.content
    return ""

    def _parse_files(self, text: str) -> dict[str, str]:
        files = {}
        pattern = r"---FILE:\s(\S+)\s---\s*(?:\w+)?\s*\n(.*?)\n"
        matches = re.findall(pattern, text, re.DOTALL)
        for path, content in matches:
            clean_path = path.strip()
            clean_content = content.strip()
            if clean_path and clean_content:
                files[clean_path] = clean_content
        return files
