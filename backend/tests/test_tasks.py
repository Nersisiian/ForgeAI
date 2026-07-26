import pytest
from httpx import AsyncClient
from app.core.security import create_access_token
from app.db.models.user import User
from app.db.models.project import Project
from app.db.models.generation_task import GenerationTask


@pytest.mark.asyncio
async def test_get_project_tasks_empty(client: AsyncClient, db_session):
    from app.core.security import get_password_hash
    user = User(email="taskuser@test.com", hashed_password=get_password_hash("test"), is_active=True)
    db_session.add(user)
    await db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    project = Project(name="P", natural_language_query="Q", target_type="fastapi", owner_id=user.id)
    db_session.add(project)
    await db_session.commit()

    response = await client.get(f"/api/v1/tasks/project/{project.id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_project_tasks_with_tasks(client: AsyncClient, db_session):
    from app.core.security import get_password_hash
    user = User(email="taskuser2@test.com", hashed_password=get_password_hash("test"), is_active=True)
    db_session.add(user)
    await db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}
    project = Project(name="P", natural_language_query="Q", target_type="fastapi", owner_id=user.id)
    db_session.add(project)
    await db_session.commit()
    task1 = GenerationTask(project_id=project.id, agent_type="planner", status="success")
    task2 = GenerationTask(project_id=project.id, agent_type="backend", status="running")
    db_session.add_all([task1, task2])
    await db_session.commit()

    response = await client.get(f"/api/v1/tasks/project/{project.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {t["agent_type"] for t in data} == {"planner", "backend"}


@pytest.mark.asyncio
async def test_forbidden_task_access(client: AsyncClient, db_session):
    from app.core.security import get_password_hash
    user1 = User(email="f1@t.com", hashed_password=get_password_hash("test"), is_active=True)
    user2 = User(email="f2@t.com", hashed_password=get_password_hash("test"), is_active=True)
    db_session.add_all([user1, user2])
    await db_session.commit()
    token1 = create_access_token({"sub": str(user1.id)})
    project = Project(name="P", natural_language_query="Q", target_type="fastapi", owner_id=user2.id)
    db_session.add(project)
    await db_session.commit()
    task = GenerationTask(project_id=project.id, agent_type="planner")
    db_session.add(task)
    await db_session.commit()

    headers = {"Authorization": f"Bearer {token1}"}
    response = await client.get(f"/api/v1/tasks/project/{project.id}", headers=headers)
    assert response.status_code == 403