from httpx import AsyncClient
from loguru import logger

from src.auth.models import User


async def test_get_users_list_access_denied(ac: AsyncClient, access_token: str):
    response = await ac.get('/superuser/get_users_list', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json()['detail'] == 'Access is denied'


async def test_get_users_list(ac: AsyncClient, super_access_token: str, super_user: User):
    response = await ac.get('/superuser/get_users_list', headers={"Authorization": f"Bearer {super_access_token}"})
    assert response.status_code == 200
    users_list = response.json()
    logger.debug(users_list)
    assert len(users_list) == 1
    assert users_list[0]['username'] == super_user.username