from httpx import AsyncClient

from src.auth.models import User


async def test_get_user_by_id_access_denied(ac: AsyncClient, access_token: str, user: User):
    response = await ac.get(f'/superuser/get_user/{user.user_id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json()['detail'] == 'Access is denied'


async def test_get_user_by_id(ac: AsyncClient, super_access_token: str, user: User):
    response = await ac.get(f'/superuser/get_user/{user.user_id}', headers={"Authorization": f"Bearer {super_access_token}"})
    assert response.status_code == 200
    assert response.json()['username'] == user.username