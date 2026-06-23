# Task tests
import pytest

@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
    r = await client.post("/tasks", json={"title": "My task", "priority": "high"}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["title"] == "My task"

@pytest.mark.asyncio
async def test_list_tasks(client, auth_headers):
    await client.post("/tasks", json={"title": "Task A"}, headers=auth_headers)
    r = await client.get("/tasks", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

@pytest.mark.asyncio
async def test_update_task(client, auth_headers):
    created = await client.post("/tasks", json={"title": "Old title"}, headers=auth_headers)
    task_id = created.json()["id"]
    r = await client.patch(f"/tasks/{task_id}", json={"title": "New title"}, headers=auth_headers)
    assert r.json()["title"] == "New title"

@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    created = await client.post("/tasks", json={"title": "To delete"}, headers=auth_headers)
    task_id = created.json()["id"]
    r = await client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert r.status_code == 204

@pytest.mark.asyncio
async def test_reorder_task(client, auth_headers):
    created = await client.post("/tasks", json={"title": "Reorder me"}, headers=auth_headers)
    task_id = created.json()["id"]
    r = await client.patch("/tasks/reorder", json={"task_id": task_id, "new_status": "in_progress", "new_position": 0}, headers=auth_headers)
    assert r.json()["status"] == "in_progress"