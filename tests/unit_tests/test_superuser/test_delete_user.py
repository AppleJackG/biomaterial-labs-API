from httpx import AsyncClient

from src.auth.models import User


async def test_get_users_list_access_denied(ac: AsyncClient, access_token: str, user: User):
    response = await ac.delete(f'/superuser/delete_user/{user.user_id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json()['detail'] == 'Access is denied'


async def test_delete_user(ac: AsyncClient, user: User, super_access_token: str):
    response = await ac.delete(f'/superuser/delete_user/{user.user_id}', headers={"Authorization": f"Bearer {super_access_token}"})
    assert response.status_code == 200
    assert response.json()['message'] == f'user {user.user_id} deleted'