
=== backend/tests/test_artifacts.py ===
```python
import pytest
from httpx import AsyncClient
from app.core.security import create_access_token
from app.db.models.user import User
from app.db.models.project import Project
from app.db.models.file_artifact import FileArtifact
from app.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_get_artifacts_empty(client: AsyncClient, db_session):
    # create user and project
    from app.core.security import get_password_hash
    user = User(
        email="artifacts@test.com",
        hashed_password=get_password_hash("test"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    project = Project(
        name="Test",
        natural_language_query="Create something",
        target_type="fastapi",
        owner_id=user.id,
    )
    db_session.add(project)
    await db_session.commit()

    # list artifacts
    response = await client.get(f"/api/v1/artifacts/project/{project.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_artifacts_with_files(client: AsyncClient, db_session):
    from app.core.security import get_password_hash
    user = User(
        email="artifacts2@test.com",
        hashed_password=get_password_hash("test"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    project = Project(
        name="Test",
        natural_language_query="Create CRM",
        target_type="fastapi",
        owner_id=user.id,
    )
    db_session.add(project)
    await db_session.commit()

    artifact = FileArtifact(
        project_id=project.id,
        file_path="src/main.py",
        content="print('hello')",
        status="draft",
    )
    db_session.add(artifact)
    await db_session.commit()

    response = await client.get(f"/api/v1/artifacts/project/{project.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["file_path"] == "src/main.py"


@pytest.mark.asyncio
async def test_update_artifact(client: AsyncClient, db_session):
    from app.core.security import get_password_hash
    user = User(
        email="artifacts3@test.com",
        hashed_password=get_password_hash("test"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    project = Project(
        name="Test",
        natural_language_query="Test",
        target_type="fastapi",
        owner_id=user.id,
    )
    db_session.add(project)
    await db_session.commit()
    artifact = FileArtifact(project_id=project.id, file_path="test.py", content="old", status="draft")
    db_session.add(artifact)
    await db_session.commit()

    update_payload = {"content": "new content", "status": "approved"}
    response = await client.put(f"/api/v1/artifacts/{artifact.id}", json=update_payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "new content"
    assert data["status"] == "approved"


@pytest.mark.asyncio
async def test_unauthorized_artifact_access(client: AsyncClient, db_session):
    from app.core.security import get_password_hash
    user1 = User(email="u1@t.com", hashed_password=get_password_hash("test"), is_active=True)
    user2 = User(email="u2@t.com", hashed_password=get_password_hash("test"), is_active=True)
    db_session.add_all([user1, user2])
    await db_session.commit()
    token1 = create_access_token({"sub": str(user1.id)})
    project = Project(name="P", natural_language_query="Q", target_type="fastapi", owner_id=user2.id)
    db_session.add(project)
    await db_session.commit()
    artifact = FileArtifact(project_id=project.id, file_path="f.py", content="c")
    db_session.add(artifact)
    await db_session.commit()

    headers = {"Authorization": f"Bearer {token1}"}
    # Trying to access user2's artifact
    response = await client.get(f"/api/v1/artifacts/project/{project.id}", headers=headers)
    assert response.status_code == 403