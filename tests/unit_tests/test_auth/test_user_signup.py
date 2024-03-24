from httpx import AsyncClient

from src.auth.models import User


async def test_user_signup(ac: AsyncClient, super_access_token: str):
    new_user = {
        "username": "test_user1",
        "password": "qwertyASD1",
        "email": "user@example.com"
    }
    response = await ac.post('/users/signup', json=new_user)
    assert response.status_code == 201
    assert response.json()['username'] == 'test_user1'
    assert response.json()['email'] == 'user@example.com'
    assert response.json()['is_superuser'] == False
    assert response.json()['is_verified'] == False
    assert response.json()['is_active'] == True
    assert 'user_id' in response.json()
    assert not ('password' in response.json())
    await ac.delete(f'/superuser/delete_user/{response.json()["user_id"]}', headers={"Authorization": f"Bearer {super_access_token}"})


async def test_user_signup_weak_password(ac: AsyncClient):
    new_user = {
        "username": "test_user2",
        "password": "qwerty",
        "email": "user@example.com"
    }
    response = await ac.post('/users/signup', json=new_user)
    assert response.status_code != 201
    assert response.json()['detail'] == 'Password is too weak'


async def test_user_signup_invalid_email(ac: AsyncClient):
    new_user = {
        "username": "test_user3",
        "password": "qwerty",
        "email": "user@example"
    }
    response = await ac.post('/users/signup', json=new_user)
    assert response.status_code != 201


async def test_user_signup_existing_username(ac: AsyncClient, user: User):
    new_user = {
        "username": user.username,
        "password": "qwertyASD1",
        "email": "userasdasd@example.com"
    }
    response = await ac.post('/users/signup', json=new_user)
    assert response.status_code != 201
    assert response.json()['detail'] == 'This username is already taken'


async def test_user_signup_existing_email(ac: AsyncClient, user: User):
    new_user = {
        "username": "test_user4",
        "password": "qwertyASD1",
        "email": user.email
    }
    response = await ac.post('/users/signup', json=new_user)
    assert response.status_code != 201
    assert response.json()['detail'] == 'This email is already taken'