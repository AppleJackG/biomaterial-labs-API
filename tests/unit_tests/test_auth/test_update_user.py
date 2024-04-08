from httpx import AsyncClient

from src.auth.models import User


async def test_update_user(ac: AsyncClient, user: User, access_token: str):
    new_values = {
        "username": "changed_username"
    }
    response = await ac.patch('/users/me', json=new_values, headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert response.json()['username'] == 'changed_username'