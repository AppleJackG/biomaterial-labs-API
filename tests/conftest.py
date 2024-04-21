from datetime import datetime, timezone
from uuid import uuid4
from src.database import Base, engine, session_factory
from src.config import settings
import pytest_asyncio
from httpx import AsyncClient
from src.main import app
from typing import AsyncGenerator
from src.auth.models import User, RefreshToken
from src.auth.utils import auth_utils

    
@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    if settings.MODE == 'TEST' or settings.MODE == 'DOCKER_TEST':
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        yield
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)
    else:
        raise ValueError(f"Not test mode: {settings.MODE}")


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def user() -> AsyncGenerator[User, None]:
    user = User()
    user.username = 'test_user'
    user.password = auth_utils.hash_password('qwertyASD1')
    user.name = 'Олег'
    user.surname = 'Вацков'
    user.role = 'student'
    async with session_factory() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    yield user
    async with session_factory() as session:
        await session.delete(user)
        await session.commit()


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


@pytest_asyncio.fixture(scope="function")
async def super_user() -> AsyncGenerator[User, None]:
    user = User()
    user.username = 'test_superuser'
    user.password = auth_utils.hash_password('qwertyASD1')
    user.name = 'Олег'
    user.surname = 'Вацков'
    user.is_superuser = True
    user.role = 'student'
    async with session_factory() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    yield user
    async with session_factory() as session:
        await session.delete(user)
        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def access_token(user: User) -> str:
    access_key = uuid4()
    access_token = auth_utils.create_access_token(user, access_key)
    return access_token


@pytest_asyncio.fixture(scope="function")
async def super_access_token(super_user: User) -> str:
    access_key = uuid4()
    access_token = auth_utils.create_access_token(super_user, access_key)
    return access_token


@pytest_asyncio.fixture(scope="function")
async def refresh_token(user: User) -> AsyncGenerator[RefreshToken, None]:
    access_key = uuid4()
    refresh_token = auth_utils.create_refresh_token(user, access_key)
    data = auth_utils.decode_token(refresh_token)
    
    token = RefreshToken()
    token.refresh_key = data.get('refresh_key')
    token.exp = datetime.fromtimestamp(data.get('exp'), timezone.utc)
    token.iat = datetime.fromtimestamp(data.get('iat'), timezone.utc)
    token.access_key = data.get('access_key')
    token.user_id = data.get('sub')

    async with session_factory() as session:
        session.add(token)
        await session.commit()
        await session.refresh(token)
    yield refresh_token
    async with session_factory() as session:
        await session.delete(token)
        await session.commit()