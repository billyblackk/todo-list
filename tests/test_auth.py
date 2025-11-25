from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


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
