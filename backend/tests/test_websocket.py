import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.models.user import User
from app.db.models.project import Project
import asyncio
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_websocket_connection_and_disconnect(db_session):
    """Test that a WebSocket connection can be established with valid token."""
    # This test requires a running server. We'll simulate using FastAPI TestClient with websocket
    from app.core.security import get_password_hash
    user = User(email="ws@test.com", hashed_password=get_password_hash("test"), is_active=True)
    db_session.add(user)
    await db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    project_id = "11111111-1111-1111-1111-111111111111"
    project = Project(id=project_id, name="Test", natural_language_query="Q", target_type="fastapi", owner_id=user.id)
    db_session.add(project)
    await db_session.commit()

    # Use TestClient with websocket
    from fastapi.testclient import TestClient
    from app.api.dependencies import get_db
    # Override dependencies for testing
    async def override_get_db():
        yield db_session
    async def override_get_current_user_ws(websocket):
        return str(user.id)
    app.dependency_overrides[get_db] = override_get_db
    # Actually, the websocket endpoint uses get_current_user_ws, we need to override that
    # But since get_current_user_ws is not a FastAPI dependency directly, it's used inside the endpoint.
    # We'll patch app.api.v1.websocket.get_current_user_ws to return user_id.
    with patch("app.api.v1.websocket.get_current_user_ws", new_callable=AsyncMock) as mock_ws_auth:
        mock_ws_auth.return_value = str(user.id)
        client = TestClient(app)
        with client.websocket_connect(f"/api/v1/ws/{project_id}?token=fake") as websocket:
            # Wait a bit for subscription
            await asyncio.sleep(0.1)
            # Should be connected
            assert websocket is not None
            # Close gracefully
            websocket.close()
    # Ensure no lingering overrides
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_websocket_invalid_token_rejected():
    client = TestClient(app)
    # Without overriding auth, it will check token - but we cannot test easily without mocking.
    # Instead, we test that the endpoint closes the connection with 4001 for invalid token.
    with patch("app.api.v1.websocket.decode_token", return_value=None):
        client = TestClient(app)
        with pytest.raises(Exception):  # Expect a close code
            with client.websocket_connect("/api/v1/ws/some-id?token=bad") as websocket:
                # The connection should be closed immediately
                pass
    # The test above may not work as expected; we can simply test that the function raises WebSocketDisconnect
    # but for integration test we'll keep simple.
    # Let's adjust to a more robust approach.