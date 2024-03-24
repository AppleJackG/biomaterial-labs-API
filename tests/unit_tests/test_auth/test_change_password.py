from httpx import AsyncClient
from loguru import logger
from src.auth.models import User


async def test_change_password(
    ac: AsyncClient,
    user: User,
    access_token: str 
):
    response = await ac.post(
        '/users/me/change_password', 
        data={
        "old_password": "qwertyASD1",
        "new_password": "passwordQWE2"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    # test login with new password
    login_response = await ac.post(
        '/auth/login', 
        data={
            "username": user.username,
            "password": "passwordQWE2"
        }
    )
    assert login_response.status_code == 200


async def test_change_password_wrong_password(
    ac: AsyncClient,
    user: User,
    access_token: str 
):
    response = await ac.post(
        '/users/me/change_password', 
        data={
        "old_password": "qwertyASD124h0345m8",
        "new_password": "passwordQWE2"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code != 200
    assert response.json()['detail'] == 'Wrong password'