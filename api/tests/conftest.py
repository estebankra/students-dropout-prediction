import pytest
from fastapi.testclient import TestClient
from fastapi_pagination import add_pagination
from httpx import Cookies

from app import database
from app.seeder import seeder
from app.database import engine, SessionLocal
from app.main import app


def get_authorization_cookie(
        test_client: TestClient, credentials: dict
) -> Cookies | None:
    response = test_client.post("/api/v1/auth/login", data=credentials)
    if response.status_code == 200:
        return response.cookies
    return None


def get_authorization_cookie_as_supervisor(
        test_client: TestClient, username: str = "supervisor"
) -> Cookies | None:
    data = {
        "username": f"{username}@supervisor.com",
        "password": "secret",
    }
    return get_authorization_cookie(test_client=test_client, credentials=data)


def get_authorization_cookie_as_admin(
        test_client: TestClient, username: str = "admin"
) -> Cookies | None:
    data = {
        "username": f"{username}@admin.com",
        "password": "secret",
    }
    return get_authorization_cookie(test_client=test_client, credentials=data)


@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def setup_database():
    # Create the database schema
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)

    # Init test database with fake data
    seeder.seed_db()

    yield

    # Drop the database schema
    database.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client(setup_database):
    # Set up a client for test
    add_pagination(app)
    client = TestClient(app)
    yield client


@pytest.fixture
def authorized_client_as_supervisor(test_client):
    authorization_cookie = get_authorization_cookie_as_supervisor(test_client)
    test_client.cookies.update(authorization_cookie)
    return test_client


@pytest.fixture
def authorized_client_as_admin(test_client):
    authorization_cookie = get_authorization_cookie_as_admin(test_client)
    test_client.cookies.update(authorization_cookie)
    return test_client
