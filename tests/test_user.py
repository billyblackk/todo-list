import pytest


def test_create_unique_user(create_test_user):
    email = "unique_pytest@example.com"
    password = "unique_pytestPassword"

    user = create_test_user(
        email=email,
        password=password,
    )

    assert user["response"].status_code == 201

    data = user["response"].json()

    assert isinstance(data["id"], int)
    assert data["email"] == email
    assert data["is_active"] is True


def test_create_duplicate_user(create_test_user):
    email = "unique_pytest@example.com"
    password = "unique_pytestPassword"

    user_1 = create_test_user(
        email=email,
        password=password,
    )

    assert user_1["response"].status_code == 201

    user_2 = create_test_user(
        email=email,
        password=password,
    )

    data = user_2["response"].json()

    assert user_2["response"].status_code == 400
    assert data["detail"] == "Email is already registered."
