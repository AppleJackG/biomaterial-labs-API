from httpx import AsyncClient

from src.auth.models import User


async def test_get_users_list_access_denied(ac: AsyncClient, access_token: str, user: User):
    response = await ac.patch(f'/superuser/update_user/{user.user_id}', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json()['detail'] == 'Access is denied'


async def test_patch_user(ac: AsyncClient, super_access_token: str, user: User):
    new_data = {
        "username": "we_patched_your_name",
    }
    response = await ac.patch(
        f'/superuser/update_user/{user.user_id}', 
        headers={"Authorization": f"Bearer {super_access_token}"},
        json=new_data
    )
    assert response.status_code == 200
    assert response.json()['username'] == 'we_patched_your_name'