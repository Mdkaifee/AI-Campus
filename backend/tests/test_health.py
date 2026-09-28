"""Phase 3 foundation tests — config, health, MongoDB."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings, get_settings
from app.main import app


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_cors_origins_parse_comma_separated(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    get_settings.cache_clear()
    settings = Settings()
    assert settings.cors_origins == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


def test_settings_defaults_ai_provider():
    settings = get_settings()
    assert settings.ai_provider in {"ollama", "openai_compatible"}
    assert settings.database_name == "Campus_AI"



@pytest.mark.asyncio
async def test_health_endpoint_with_lifespan():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"ok", "degraded"}
    assert payload["database"] in {"ok", "unavailable"}
    # Prefer connected DB when Atlas credentials/network are valid
    if payload["database"] == "ok":
        assert payload["status"] == "ok"
