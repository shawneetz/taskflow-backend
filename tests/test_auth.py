# Auth tests
import pytest

@pytest.mark.asyncio
async def test_register_success(client):
    r = await client.post("/auth/register", json={"email": "new@x.com", "password": "password123", "full_name": "New"})
    assert r.status_code == 201
    assert r.json()["email"] == "new@x.com"

@pytest.mark.asyncio
async def test_register_duplicate_email(client, test_user):
    r = await client.post("/auth/register", json={"email": "test@example.com", "password": "password123", "full_name": "Dup"})
    assert r.status_code == 409

@pytest.mark.asyncio
async def test_login_success(client, test_user):
    r = await client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert "refresh_token" in r.json()

@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user):
    r = await client.post("/auth/login", json={"email": "test@example.com", "password": "wrongpass"})
    assert r.status_code == 401

@pytest.mark.asyncio
async def test_get_me(client, auth_headers):
    r = await client.get("/users/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "test@example.com"