from typing import Generator

import pytest
from tortoise.contrib.test import initializer, finalizer
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def init_db() -> Generator:
    initializer(["app.models"], db_url="sqlite://test.sqlite3")
    yield
    finalizer()
