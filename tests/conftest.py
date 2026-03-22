import asyncio
import os
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_banco_api.db"

from app import models  # noqa: F401
from app.db.base import Base
from app.db.session import engine
from app.main import app


TEST_DB_PATH = Path("test_banco_api.db")


def _run(coro):
    return asyncio.run(coro)


async def _reset_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True)
def reset_database():
    _run(_reset_database())


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client: TestClient):
    username = f"user_{uuid4().hex[:8]}"
    password = "123456"

    register_response = client.post(
        "/auth/register",
        json={"username": username, "password": password},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    yield
    _run(engine.dispose())
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink(missing_ok=True)
