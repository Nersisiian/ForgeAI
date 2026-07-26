import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.planner import PlannerAgent
from app.agents.architect import ArchitectAgent
from app.agents.backend_generator import BackendGeneratorAgent
from app.agents.frontend_generator import FrontendGeneratorAgent
from app.agents.database_generator import DatabaseGeneratorAgent
from app.agents.docker_generator import DockerGeneratorAgent
from app.agents.testing_generator import TestingGeneratorAgent
from app.agents.documentation_generator import DocumentationGeneratorAgent
from app.agents.review_agent import ReviewAgent
from app.agents.fix_agent import FixAgent
from app.db.models.project import Project
from app.db.models.generation_task import GenerationTask
from app.db.models.file_artifact import FileArtifact
from app.services.llm_service import LLMService


@pytest.mark.asyncio
async def test_planner_agent_execute(db_session):
    project = Project(
        id=uuid4(),
        name="Test",
        natural_language_query="Build CRM",
        target_type="fastapi",
        owner_id=uuid4(),
    )
    task = GenerationTask(id=uuid4(), project_id=project.id, agent_type="planner")
    db_session.add_all([project, task])
    await db_session.commit()

    with patch.object(LLMService, "generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "# Plan\nThis is a plan."
        agent = PlannerAgent(db_session, task.id, project.id)
        await agent.execute()

    # Check artifact created
    artifacts = (await db_session.execute(
        __import__('sqlalchemy').select(FileArtifact).where(FileArtifact.project_id == project.id)
    )).scalars().all()
    assert len(artifacts) == 1
    assert artifacts[0].file_path == "PLAN.md"
    assert "# Plan" in artifacts[0].content


@pytest.mark.asyncio
async def test_architect_agent_execute(db_session):
    project = Project(id=uuid4(), name="Test", natural_language_query="Build CRM", target_type="fastapi", owner_id=uuid4())
    task = GenerationTask(id=uuid4(), project_id=project.id, agent_type="architect")
    db_session.add_all([project, task])
    await db_session.commit()

    with patch.object(LLMService, "generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "# Architecture\nDetailed spec."
        agent = ArchitectAgent(db_session, task.id, project.id)
        await agent.execute()

    artifacts = (await db_session.execute(
        __import__('sqlalchemy').select(FileArtifact).where(FileArtifact.project_id == project.id, FileArtifact.file_path == "ARCHITECTURE.md")
    )).scalars().all()
    assert len(artifacts) == 1
    assert "Architecture" in artifacts[0].content


@pytest.mark.asyncio
async def test_backend_generator_parse_files(db_session):
    project = Project(id=uuid4(), name="Test", natural_language_query="API", target_type="fastapi", owner_id=uuid4())
    task = GenerationTask(id=uuid4(), project_id=project.id, agent_type="backend")
    db_session.add_all([project, task])
    await db_session.commit()

    mock_response = (
        "---FILE: main.py---\n"
        "```python\n"
        "print('hello')\n"
        "```\n"
        "---FILE: models.py---\n"
        "```python\n"
        "class User:\n    pass\n"
        "```"
    )
    with patch.object(LLMService, "generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = mock_response
        # also mock validation to always pass
        with patch.object(BackendGeneratorAgent, "_validate_and_fix", new_callable=AsyncMock) as mock_validate:
            mock_validate.side_effect = lambda path, content, tid: content
            agent = BackendGeneratorAgent(db_session, task.id, project.id)
            await agent.execute()

    artifacts = (await db_session.execute(
        __import__('sqlalchemy').select(FileArtifact).where(FileArtifact.project_id == project.id)
    )).scalars().all()
    paths = [a.file_path for a in artifacts]
    assert "main.py" in paths
    assert "models.py" in paths


@pytest.mark.asyncio
async def test_frontend_generator_execute(db_session):
    project = Project(id=uuid4(), name="Test", natural_language_query="UI", target_type="fastapi", owner_id=uuid4())
    task = GenerationTask(id=uuid4(), project_id=project.id, agent_type="frontend")
    db_session.add_all([project, task])
    await db_session.commit()

    mock_response = (
        "---FILE: src/App.tsx---\n"
        "```tsx\n"
        "import React from 'react';\n"
        "export default function App() { return <div>Hello</div>; }\n"
        "```"
    )
    with patch.object(LLMService, "generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = mock_response
        agent = FrontendGeneratorAgent(db_session, task.id, project.id)
        await agent.execute()

    artifacts = (await db_session.execute(
        __import__('sqlalchemy').select(FileArtifact).where(FileArtifact.project_id == project.id)
    )).scalars().all()
    assert any(a.file_path == "src/App.tsx" for a in artifacts)


@pytest.mark.asyncio
async def test_review_agent_finds_issues(db_session):
    project = Project(id=uuid4(), name="Test", natural_language_query="X", target_type="fastapi", owner_id=uuid4())
    task = GenerationTask(id=uuid4(), project_id=project.id, agent_type="review")
    bad_artifact = FileArtifact(
        id=uuid4(), project_id=project.id, task_id=task.id,
        file_path="bad.py", content="def f(): pass\nx=1", status="draft"
    )
    db_session.add_all([project, task, bad_artifact])
    await db_session.commit()

    with patch.object(ReviewAgent, "validator") as mock_validator:
        mock_validator.lint_code = AsyncMock(return_value=(False, ["E302 expected 2 blank lines"]))
        agent = ReviewAgent(db_session, task.id, project.id)
        issues = await agent.review()
        assert len(issues) == 1
        assert issues[0]["file"] == "bad.py"
        assert "E302" in str(issues[0]["errors"])


@pytest.mark.asyncio
async def test_fix_agent_repairs_artifact(db_session):
    project = Project(id=uuid4(), name="Test", natural_language_query="X", target_type="fastapi", owner_id=uuid4())
    task = GenerationTask(id=uuid4(), project_id=project.id, agent_type="fix", input_data={"issues": [{"file": "bad.py", "errors": ["E302"]}]})
    artifact = FileArtifact(
        id=uuid4(), project_id=project.id, file_path="bad.py",
        content="def f(): pass\nx=1", status="draft"
    )
    db_session.add_all([project, task, artifact])
    await db_session.commit()

    with patch.object(LLMService, "generate", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "def f(): pass\n\nx=1"
        with patch.object(FixAgent, "validator") as mock_validator:
            mock_validator.lint_code = AsyncMock(return_value=(True, []))
            agent = FixAgent(db_session, task.id, project.id)
            await agent.execute()

    # reload artifact
    await db_session.refresh(artifact)
    assert artifact.content == "def f(): pass\n\nx=1"
    assert artifact.status == "approved"