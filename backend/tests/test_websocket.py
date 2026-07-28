import asyncio
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.db.models.user import User
from app.db.models.project import Project
from app.core.security import get_password_hash

@pytest.mark.asyncio
async def test_websocket_connection_and_disconnect(db_session):
    user = User(
        email="ws@test.com",
        hashed_password=get_password_hash("test"),
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    project_id = "11111111-1111-1111-1111-111111111111"
    project = Project(
        id=project_id,
        name="Test",
        natural_language_query="Q",
        target_type="fastapi",
        owner_id=user.id,
    )
    db_session.add(project)
    await db_session.commit()

    # Импортируем app после того, как база готова (уже в test_app)
    from app.main import app

    client = TestClient(app)
    with patch("app.api.v1.websocket.decode_token", return_value={"sub": str(user.id)}):
        with client.websocket_connect(f"/api/v1/ws/{project_id}?token=fake") as websocket:
            await asyncio.sleep(0.1)
            assert websocket is not None
            websocket.close()

@pytest.mark.asyncio
async def test_websocket_invalid_token_rejected():
    with patch("app.api.v1.websocket.decode_token", return_value=None):
        from app.main import app
        client = TestClient(app)
        with pytest.raises(Exception):
            with client.websocket_connect("/api/v1/ws/some-id?token=bad") as _:
                pass
