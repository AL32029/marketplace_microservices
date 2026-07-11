import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from user_service.bootstrap import build_services
from user_service.infrastructure.config import JWTSettings
from user_service.infrastructure.db.models import Base
from user_service.presentation.api.user_router import router


@pytest.fixture(scope='session')
async def client():
    app = FastAPI()
    app.include_router(router)

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    app.state.db_session = session_maker

    jwt_settings = JWTSettings()
    app.state.services = build_services(jwt_settings)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    await engine.dispose()


@pytest.mark.asyncio
async def test_full_auth_flow(client):
    resp = await client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "secure_password_123",
        "full_name": "Test User"
    })
    assert resp.status_code == 200
    user = resp.json()
    assert user["email"] == "test@example.com"

    resp = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "secure_password_123"
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    headers = {"Authorization": f"Bearer {token}"}
    resp = await client.get("/users/me", headers=headers)
    assert resp.status_code == 200
    profile = resp.json()
    assert profile["email"] == "test@example.com"
    assert profile["full_name"] == "Test User"
