from httpx import AsyncClient

from src.auth.models import User


async def test_logout(ac: AsyncClient, user: User):
    first_login = await ac.post('/auth/login', data={'username': user.username, 'password': 'qwertyASD1'})
    assert first_login.status_code == 200
    refresh_token = first_login.json()['refresh_token']
    access_token = first_login.json()['access_token']

    logout_response = await ac.post('/auth/logout', headers={'Authorization': f'Bearer {access_token}'})
    assert logout_response.status_code == 200

    refresh_response = await ac.post('/auth/refresh', headers={'refresh-token': refresh_token})
    assert refresh_response.status_code == 403