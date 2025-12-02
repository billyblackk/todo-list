import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

os.environ["TESTING"] = "1"

# Create a test database so that the database in dev isnt contaminated
SQLALCHEMY_TEST_URL = "sqlite:///.test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def create_test_user(client):
    def _create_test_user(email: str, password: str):
        payload = {
            "email": email,
            "password": password,
        }

        response = client.post("/users/", json=payload)

        return {
            "email": email,
            "password": password,
            "response": response,
        }

    return _create_test_user


@pytest.fixture(scope="function")
def user_login(client):
    def _user_login(username: str, password: str):
        payload = {
            "username": username,
            "password": password,
        }

        response = client.post("/auth/login", data=payload)

        return {
            "username": username,
            "password": password,
            "response": response,
        }

    return _user_login


@pytest.fixture(scope="function")
def auth_headers(create_test_user, user_login):
    def _auth_headers(email: str, password: str):
        user = create_test_user(email, password)
        login = user_login(username=email, password=password)
        data = login["response"].json()
        return {"Authorization": f"Bearer {data['access_token']}"}

    return _auth_headers


@pytest.fixture(scope="function")
def db_session():
    """
    Before each test, tables are recreated fresh.
    This way we can keep the tests isolated and repeat
    tests without having to change the test cases
    Also the database in dev is not contaminated with test data.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
