from uuid import UUID

from .models import User, RefreshToken
from sqlalchemy import delete, select, insert, update
from sqlalchemy.orm import joinedload
from ..database import session_factory
from .utils import auth_utils
from datetime import datetime, timezone



class AuthRepository:
    
    @staticmethod
    async def add_refresh_token(token: str) -> None:
        data = auth_utils.decode_token(token)
        new_data = {
            'refresh_key': data.get('refresh_key'),
            'exp': datetime.fromtimestamp(data.get('exp'), timezone.utc),
            'iat': datetime.fromtimestamp(data.get('iat'), timezone.utc),
            'access_key': data.get('access_key'),
            'user_id': data.get('sub')
        }
        stmt = insert(RefreshToken).values(**new_data)
        async with session_factory() as session:
            await session.execute(stmt)
            await session.commit()
        return None

    @staticmethod
    async def find_refresh_token(payload: dict) -> RefreshToken | None:
        query = (
            select(RefreshToken)
            .where(
                RefreshToken.access_key == payload.get('access_key'),
                RefreshToken.refresh_key == payload.get('refresh_key'),
                RefreshToken.exp > datetime.now(timezone.utc)
            )
            .options(joinedload(RefreshToken.user))
        )
        async with session_factory() as session:
            result = await session.execute(query)
            if refresh_token := result.scalar_one_or_none():
                refresh_token.exp = datetime.now(timezone.utc)
            await session.commit()
        return refresh_token
    
    @staticmethod
    async def deactivate_refresh_token(user_id: UUID) -> None:
        query = (
            select(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.exp > datetime.now(timezone.utc)
            )
        )
        async with session_factory() as session:
            result = await session.execute(query)
            tokens = result.scalars()
            for token in tokens:
                token.exp = datetime.now(timezone.utc)
            await session.commit()


class UserRepository:
    
    @staticmethod
    async def get_user_by_username(username: str) -> User | None:
        query = select(User).where(User.username == username)
        async with session_factory() as session:
            result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> User | None:
        query = select(User).where(User.user_id == user_id)
        async with session_factory() as session:
            result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
    
    @staticmethod
    async def create_new_user(new_user_data: dict[str, str]) -> User:
        stmt = insert(User).values(**new_user_data).returning(User)
        async with session_factory() as session:
            result = await session.execute(stmt)
            await session.commit()
        created_user = result.scalar_one()
        return created_user
    
    @staticmethod
    async def update_user(user_id: UUID, new_data_dict: dict) -> User:
        stmt = (
            update(User)
            .where(User.user_id == user_id)
            .values(**new_data_dict)
            .returning(User)
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            user = result.scalar_one()
            await session.commit()
        return user
    

    @staticmethod
    async def delete_user(user_id: UUID) -> None:
        stmt = delete(User).where(User.user_id == user_id)
        async with session_factory() as session:
            await session.execute(stmt)
            await session.commit()
        return None
    
    @staticmethod
    async def get_users_list(offset: int = 0, limit: int = 100) -> list[User]:
        query = select(User).limit(limit).offset(offset)
        async with session_factory() as session:
            result = await session.execute(query)
        users = result.scalars()
        return users


auth_repository = AuthRepository()
user_repository = UserRepository()
