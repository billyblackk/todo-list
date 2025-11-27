import pytest


def test_successful_login(create_test_user, user_login):
    user = create_test_user(
        email="login_pytest@example.com",
        password="login_pytest_password",
    )

    assert user["response"].status_code == 201

    login_response = user_login(
        username=user["email"],
        password=user["password"],
    )

    data = login_response["response"].json()

    assert login_response["response"].status_code == 200
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert data["access_token"]


def test_unsuccessful_login_username(create_test_user, user_login):
    user = create_test_user(
        email="login_pytest@example.com",
        password="login_pytest_password",
    )

    assert user["response"].status_code == 201

    login_response = user_login(
        username="wrong_username",
        password=user["password"],
    )

    response = login_response["response"]

    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"


def test_unsuccessful_login_password(create_test_user, user_login):
    user = create_test_user(
        email="login_pytest@example.com",
        password="login_pytest_password",
    )

    assert user["response"].status_code == 201

    login_response = user_login(
        username=user["email"],
        password="wrong_password",
    )

    response = login_response["response"]

    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"
