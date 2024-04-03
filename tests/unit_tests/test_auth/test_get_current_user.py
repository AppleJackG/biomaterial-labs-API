from httpx import AsyncClient

from src.auth.models import User


async def test_get_current_user(ac: AsyncClient, user: User, access_token: str):
    response = await ac.get('/users/me', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()['username'] == user.username
    assert response.json()['is_superuser'] == user.is_superuser
    assert response.json()['is_verified'] == user.is_verified
    assert response.json()['is_active'] == user.is_active
    assert response.json()['user_id'] == str(user.user_id)
    assert response.json()['role'] == str(user.role)
