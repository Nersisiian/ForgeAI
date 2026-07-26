import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    # login first
    reg = await client.post("/api/v1/auth/register", json={"email": "p@test.com", "password": "pass1234"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    proj_data = {
        "name": "Test CRM",
        "natural_language_query": "Create CRM for dental clinic",
        "target_type": "fastapi",
    }
    resp = await client.post("/api/v1/projects/", json=proj_data, headers=headers)
    assert resp.status_code == 201
    project = resp.json()
    assert project["name"] == "Test CRM"
    # list
    list_resp = await client.get("/api/v1/projects/", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()["items"]) >= 1