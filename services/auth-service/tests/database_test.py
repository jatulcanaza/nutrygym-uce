import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.types import TypeDecorator, CHAR

from app.core.database import Base
from app.models.user import UserDB


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


class GUID(TypeDecorator):

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


for column in UserDB.__table__.columns:

    if column.name == "id":
        column.type = GUID()


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)