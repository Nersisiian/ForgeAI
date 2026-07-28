import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_create_project(client: AsyncClient):
    reg_data = {"email": "p@test.com", "password": "pass1234"}
    resp = await client.post("/api/v1/auth/register", json=reg_data)
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens

    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    proj_data = {
        "name": "Test CRM",
        "natural_language_query": "Create CRM for dental clinic",
        "target_type": "fastapi",
    }
    resp = await client.post("/api/v1/projects/", json=proj_data, headers=headers)
    assert resp.status_code == 201
    project = resp.json()
    assert project["name"] == "Test CRM"
