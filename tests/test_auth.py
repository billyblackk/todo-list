import pytest

# -----------
# User Auth
# -----------


def test_successful_login(client, create_test_user):
    user = create_test_user(
        email="login_pytest@example.com",
        password="login_pytest_password",
    )

    # login with OAuth2PasswordRequestForm, so use a form, not json
    login_response = client.post(
        "/auth/login", data={"username": user["email"], "password": user["password"]}
    )
    data = login_response.json()

    assert login_response.status_code == 200
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert data["access_token"]


def test_unsuccessful_login_username(client, create_test_user):
    user = create_test_user(
        email="login_pytest@example.com",
        password="login_pytest_password",
    )

    # login with OAuth2PasswordRequestForm, so use a form, not json
    login_response = client.post(
        "/auth/login",
        data={"username": "wrong_username", "password": user["password"]},
    )

    assert login_response.status_code == 401
    assert login_response.headers.get("WWW-Authenticate") == "Bearer"


def test_unsuccessful_login_password(client, create_test_user):
    user = create_test_user(
        email="login_pytest@example.com",
        password="login_pytest_password",
    )

    # login with OAuth2PasswordRequestForm, so use a form, not json
    login_response = client.post(
        "/auth/login",
        data={"username": user["email"], "password": "wrong_password"},
    )

    assert login_response.status_code == 401
    assert login_response.headers.get("WWW-Authenticate") == "Bearer"
