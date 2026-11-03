from collections.abc import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from relay.config import Settings
from relay.main import create_app


@pytest.fixture
def settings() -> Settings:
    # init kwargs beat env vars; _env_file=None ignores the developer's .env
    return Settings(environment="testing", _env_file=None)


@pytest.fixture
async def client(settings: Settings) -> AsyncIterator[AsyncClient]:
    app = create_app(settings)
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac
