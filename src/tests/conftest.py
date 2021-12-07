from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from dependency import get_db
from decouple import config
from typing import Any, Generator
from database import Base
from tests.utils.user import fetch_test_user_auth_header
import pytest

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./bucket-list-test.db"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db_session() -> Generator[TestingSessionLocal, Any, None]:
    """
    Description: Create the db_session Pytest Fixture for testing.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session  # use the session in tests.
    # Cleaning up transactions
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db_session: TestingSessionLocal) -> Generator[TestClient, Any, None]:
    """
    Description: Pytest fixture for the FastAPI Test Client
    """
    # Override the base db session dependency to use the testing session
    # This overrides the `get_db` dependency which is injected into routes for testing purposes only
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # Dependency override
    app.dependency_overrides[get_db] = override_get_db

    # Generate the client
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def create_test_user_auth_header(client: TestClient, db_session: TestingSessionLocal):
    """
    Description: Pytest Fixture for the test user authorization header
    """
    return fetch_test_user_auth_header(client, db_session)
