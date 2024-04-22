from typing import AsyncGenerator
from httpx import AsyncClient
import pytest_asyncio
from src.auth.models import User
from src.config import settings
from src.auth.utils import auth_utils
from src.database import session_factory


@pytest_asyncio.fixture(scope="function")
async def inactive_user() -> AsyncGenerator[User, None]:
    user = User()
    user.username = 'test_inactive_user'
    user.password = auth_utils.hash_password('qwertyASD1')
    user.name = 'Олег'
    user.surname = 'Вацков'
    user.is_active = False
    user.role = 'student'
    async with session_factory() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    yield user
    async with session_factory() as session:
        await session.delete(user)
        await session.commit()

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