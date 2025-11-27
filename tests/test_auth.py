from fastapi.testclient import TestClient
from app.main import app
from app.routers.auth import login


def test_create_unique_user(client):
    payload = {
        "email": "unique_pytest@example.com",
        "password": "unique_pytestPassword",
    }

    client.post("/users/", json=payload)
    response = client.post("/users/", json=payload)

    data = response.json()

    assert response.status_code == 201
    assert isinstance(data["id"], int)
    assert data["email"] == payload["email"]
    assert data["is_active"] is True


def test_create_duplicate_user(client):
    payload = {
        "email": "duplicate_pytest@example.com",
        "password": "duplicate_pytestPassword",
    }

    first = client.post("/users/", json=payload)
    assert first.status_code == 201

    second = client.post("/users/", json=payload)
    data = second.json()

    assert second.status_code == 400
    assert data["detail"] == "Email is already registered."


def test_get_task_correct_user(client):
    payload = {
        "email": "duplicate_pytest@example.com",
        "password": "duplicate_pytestPassword",
    }

    first = client.post("/users/", json=payload)
    assert first.status_code == 201


def test_get_task_wrong_user(client):
    # register with user 1
    user1_payload = {
        "email": "user1_pytest@example.com",
        "password": "user1_pytestPassword",
    }

    register_response_1 = client.post("/users/", json=user1_payload)
    assert register_response_1.status_code == 201

    # log in with user 1

    # add task as user 1

    # register with user 2
    user2_payload = {
        "email": "user2_pytest@example.com",
        "password": "user2_pytestPassword",
    }

    register_response_2 = client.post("/users/", json=user2_payload)
    assert register_response_2.status_code == 201
    # log in with user 2
    # add task as user 2
