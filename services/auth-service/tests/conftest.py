import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest

from fastapi.testclient import TestClient

from main import app

from app.core.database import get_db

from tests.database_test import (
    TestingSessionLocal,
    Base,
    engine,
)


Base.metadata.create_all(bind=engine)


def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():

    with TestClient(app) as c:
        yield c