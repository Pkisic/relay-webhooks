import logging

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pydantic import ValidationError

from relay.config import Settings
from relay.main import create_app


async def test_health_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_openapi_documents_health_response(client: AsyncClient) -> None:
    schema = (await client.get("/openapi.json")).json()

    assert "HealthResponse" in schema["components"]["schemas"]


async def test_apps_with_different_settings_coexist() -> None:
    first = create_app(Settings(app_name="First", _env_file=None))
    second = create_app(Settings(app_name="Second", _env_file=None))

    assert first.title == "First"
    assert second.title == "Second"


async def test_lifespan_logs_startup_and_shutdown(
    settings: Settings, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO, logger="relay.main")

    async with LifespanManager(create_app(settings)):
        pass

    messages = [r.getMessage() for r in caplog.records]
    assert any("starting" in m for m in messages)
    assert any("shutting down" in m for m in messages)


def test_invalid_environment_fails_at_startup() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="prodcution", _env_file=None)
