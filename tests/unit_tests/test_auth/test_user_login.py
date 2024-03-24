from httpx import AsyncClient
from src.auth.models import User
from src.config import settings


async def test_user_login(ac: AsyncClient, user: User):
    login_data = {
        "username": user.username,
        "password": "qwertyASD1"
    }
    response = await ac.post('/auth/login', data=login_data)
    assert response.status_code == 200
    assert response.json()['access_token'] is not None
    assert response.json()['refresh_token'] is not None
    assert response.json()['expires_in'] == settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    assert response.json()['token_type'] == 'Bearer'


async def test_user_login_wrong_password(ac: AsyncClient, user: User):
    login_data = {
        "username": user.username,
        "password": "ugh340diu"
    }
    response = await ac.post('/auth/login', data=login_data)
    assert response.status_code != 200
    assert response.json()['detail'] == 'Invalid username or password'


async def test_user_login_wrong_username(ac: AsyncClient, user: User):
    login_data = {
        "username": 'wreonklgdf',
        "password": "afsasdh34y45"
    }
    response = await ac.post('/auth/login', data=login_data)
    assert response.status_code != 200
    assert response.json()['detail'] == 'Invalid username or password'


async def test_user_login_inactive_user(ac: AsyncClient, inactive_user: User):
    login_data = {
        "username": inactive_user.username,
        "password": "qwertyASD1"
    }
    response = await ac.post('/auth/login', data=login_data)
    assert response.status_code != 200
    assert response.json()['detail'] == 'Inactive user'