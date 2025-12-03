import pytest


def test_create_task_for_current_user(client, auth_headers):
    headers = auth_headers(email="taskTest@example.com", password="taskTest_password")

    task = {
        "title": "Test task",
        "description": "Test task to see if we can create a task for a user",
        "is_donee": False,
    }

    create_task_response = client.post("/tasks/", json=task, headers=headers)
    create_task_data = create_task_response.json()

    print(create_task_data)

    assert create_task_response.status_code == 201
    assert create_task_data["title"] == task["title"]
    assert create_task_data["description"] == task["description"]
    assert create_task_data["is_done"] is False


def test_list_tasks_for_current_user(client, auth_headers):
    headers = auth_headers(email="taskTest@example.com", password="taskTest_password")

    tasks = [
        {
            "title": "Test task 1",
            "description": "Test task 1",
            "is_donee": False,
        },
        {
            "title": "Test task 2",
            "description": "Test task 2",
            "is_donee": False,
        },
        {
            "title": "Test task 3",
            "description": "Test task 3",
            "is_donee": False,
        },
        {
            "title": "Test task 4",
            "description": "Test 4",
            "is_donee": False,
        },
    ]

    for task in tasks:
        client.post("/tasks/", json=task, headers=headers)

    list_all_tasks_response = client.get("/tasks/", headers=headers)
    list_all_tasks_data = list_all_tasks_response.json()

    print(list_all_tasks_data)

    assert list_all_tasks_response.status_code == 200
    assert len(list_all_tasks_data) == len(tasks)
    for task, response_data in zip(tasks, list_all_tasks_data):
        assert task["title"] == response_data["title"]


# def test_get_task_for_current_user_by_id(client, auth_headers):
# def test_update_task_for_current_user_by_id():
# def test_cant_get_tasks_by_other_user():
#%%