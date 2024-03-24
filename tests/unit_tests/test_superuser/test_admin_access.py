from httpx import AsyncClient

from src.auth.models import User


async def test_admin_access_denied(ac: AsyncClient, user: User):
    credentials = {
        "username": user.username,
        "password": "qwertyASD1"
    }
    response = await ac.post('/admin/login', data=credentials)
    assert response.status_code == 403


async def test_admin_access(ac: AsyncClient, super_user: User):
    credentials = {
        "username": super_user.username,
        "password": "qwertyASD1"
    }
    response = await ac.post('/admin/login', data=credentials)
    assert response.status_code == 302