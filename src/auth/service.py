from uuid import UUID, uuid4
from fastapi import Depends, HTTPException, status
from loguru import logger
from .repository import AuthRepository, user_repository, UserRepository, auth_repository
from .models import User
from typing import NoReturn
from .utils import auth_utils
from .schemas import Token, UserCreate, RefreshTokenPayload, UserPatch, UserSchema, UserUpdate, VerifyUserEmailSchema
from .exceptions import InvalidCredentials, InvalidToken, UsernameIsTaken, EmailIsTaken
from ..config import settings
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


class AuthService:

    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository) -> None:
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    async def login(self, username: str, password: str) -> Token | NoReturn:
        user = await self.user_repo.get_user_by_username(username)
        if auth_utils.check_credentials(user, password):
            access_key = uuid4()
            access_token = auth_utils.create_access_token(user, access_key)
            refresh_token = auth_utils.create_refresh_token(user, access_key)
            await self.auth_repo.add_refresh_token(refresh_token)
            return Token(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type='Bearer',
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        
    async def refresh_token(self, refresh_token: str) -> Token:
        payload = auth_utils.decode_token(refresh_token)
        if not (token_in_db := await self.auth_repo.find_refresh_token(payload)):
            raise InvalidToken
        new_access_key = uuid4()
        new_access_token = auth_utils.create_access_token(token_in_db.user, new_access_key)
        new_refresh_token = auth_utils.create_refresh_token(token_in_db.user, new_access_key)
        await self.auth_repo.add_refresh_token(new_refresh_token)
        return Token(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                token_type='Bearer',
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
    
    async def logout(self, user: UserSchema) -> None:
        await auth_repository.deactivate_refresh_token(user.user_id)
    

class UserService:
    
    def __init__(self, user_repo: UserRepository) -> None:
        self.repo = user_repo

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> User:
        payload = auth_utils.decode_token(token)
        user_id: UUID | None = payload.get('sub')
        user = await self.repo.get_user_by_id(user_id)
        return user
    
    async def get_current_superuser(self, token: str = Depends(oauth2_scheme)) -> User | NoReturn:
        payload = auth_utils.decode_token(token)
        user_id: UUID | None = payload.get('sub')
        user = await self.repo.get_user_by_id(user_id)
        if not user.is_superuser == True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Access is denied'
            )
        return user
    
    async def check_admin_rights(self, username: str, password: str) -> bool | NoReturn:
        user = await self.repo.get_user_by_username(username)
        if not user:
            raise InvalidCredentials
        if not user.is_superuser == True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Access is denied'
            )
        if auth_utils.check_credentials(user, password):
            return True
        return False
    
    async def register_new_user(self, user_data: UserCreate) -> User | NoReturn:
        if not auth_utils.check_password_strength(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password is too weak'
            )
        user_dict = user_data.model_dump(exclude_unset=True)
        user_dict.update(
            {'password': auth_utils.hash_password(user_data.password)}
        )
        user_exists = await self.repo.get_user_by_username(user_dict.get('username'))
        if user_exists:
            raise UsernameIsTaken
        if email := user_dict.get('email'):
            user_exists = await self.repo.get_user_by_email(email)
            if user_exists:
                raise EmailIsTaken
        new_user = await self.repo.create_new_user(user_dict)
        return new_user
    
    async def change_password(
        self,
        user: User,
        old_password: str,
        new_password: str
    ) -> User:
        if not auth_utils.validate_password(old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Wrong password'
            )
        if not auth_utils.check_password_strength(new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password is too weak'
            )
        new_data_dict = {
            'password': auth_utils.hash_password(new_password)
        }
        user = await self.repo.update_user(user.user_id, new_data_dict)
        return user
    
    async def patch_user(self, user_id: UUID, new_values: UserPatch | UserUpdate) -> User:
        new_data_dict = new_values.model_dump(exclude_unset=True)
        user = await self.repo.update_user(user_id, new_data_dict)
        return user

    async def delete_user(self, user_id: UUID) -> None:
        await self.repo.delete_user(user_id)
        return None
    
    async def get_users_list(self, offset: int = 0, limit: int = 100) -> list[User]:
        users = await self.repo.get_users_list(offset, limit)
        return users
    
    async def get_user_by_id(self, user_id: UUID) -> User:
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        return user


auth_service = AuthService(auth_repository, user_repository)
user_service = UserService(user_repository)