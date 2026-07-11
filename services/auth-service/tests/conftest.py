import pytest
import uuid

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.types import TypeDecorator, CHAR

from main import app
from app.core.database import Base, get_db
from app.models.user import UserDB


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


class GUID(TypeDecorator):
    """
    Compatible UUID para SQLite durante pruebas.
    Mantiene UUID real en PostgreSQL.
    """

    impl = CHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):

        if value is None:
            return None

        if isinstance(value, uuid.UUID):
            return str(value)

        return str(uuid.UUID(value))


    def process_result_value(self, value, dialect):

        if value is None:
            return None

        return uuid.UUID(value)



# Reemplazar UUID PostgreSQL por GUID para SQLite
for column in UserDB.__table__.columns:
    if column.name == "id":
        column.type = GUID()



engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
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