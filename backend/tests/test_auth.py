import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    reg_data = {"email": "test@example.com", "password": "Str0ng!Pass"}
    resp = await client.post("/api/v1/auth/register", json=reg_data)
    assert resp.status_code == 200
    tokens = resp.json()
    assert "access_token" in tokens

    login_resp = await client.post("/api/v1/auth/login", json=reg_data)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()