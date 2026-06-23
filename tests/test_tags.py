# Tag tests
import pytest

@pytest.mark.asyncio
async def test_create_tag(client, auth_headers):
    r = await client.post("/tags", json={"name": "frontend", "color": "#6366f1"}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["name"] == "frontend"

@pytest.mark.asyncio
async def test_duplicate_tag_name(client, auth_headers):
    await client.post("/tags", json={"name": "dupe", "color": "#6366f1"}, headers=auth_headers)
    r = await client.post("/tags", json={"name": "dupe", "color": "#6366f1"}, headers=auth_headers)
    assert r.status_code == 409

@pytest.mark.asyncio
async def test_delete_tag(client, auth_headers):
    created = await client.post("/tags", json={"name": "to-delete", "color": "#6366f1"}, headers=auth_headers)
    tag_id = created.json()["id"]
    r = await client.delete(f"/tags/{tag_id}", headers=auth_headers)
    assert r.status_code == 204