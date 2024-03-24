from typing import NoReturn
from uuid import UUID, uuid4
import jwt
from jwt.exceptions import ExpiredSignatureError
from .exceptions import ExpiredToken, InactiveUser, InvalidCredentials, InvalidToken
from .schemas import AccessTokenPayload, RefreshTokenPayload
from .models import User
from ..config import settings
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


class AuthUtilities:

    @staticmethod
    def encode_token(
        payload: dict,
        private_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM
    ) -> str:
        encoded = jwt.encode(payload, private_key, algorithm=algorithm)
        return encoded
    
    @staticmethod
    def decode_token(
        token: str,
        public_key: str = settings.PUBLIC_KEY,
        algorithm: str = settings.ALGORITHM
    ) -> dict:
        try:
            decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        except ExpiredSignatureError:
            raise ExpiredToken
        except jwt.InvalidTokenError:
            raise InvalidToken
        return decoded

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)
    
    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password
        )
    
    @staticmethod
    def check_credentials(user: User | None, password: str) -> bool | NoReturn:
        if not user:
            raise InvalidCredentials
        if not auth_utils.validate_password(password, user.password):
            raise InvalidCredentials
        if not user.is_active:
            raise InactiveUser
        return True   
    
    @classmethod
    def create_access_token(cls, user: User, access_key: UUID) -> str:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_payload = AccessTokenPayload(
            sub=str(user.user_id),
            username=user.username,
            email=user.email,
            exp=expire_time,
            iat=datetime.now(timezone.utc),
            access_key=str(access_key)
        )
        to_encode = access_token_payload.model_dump()
        access_token = cls.encode_token(to_encode)
        return access_token
    
    @classmethod
    def create_refresh_token(cls, user: User, access_key: UUID) -> str:
        expire_time = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token_payload = RefreshTokenPayload(
            sub=str(user.user_id),
            access_key=str(access_key),
            refresh_key=str(uuid4()),
            exp=expire_time,
            iat=datetime.now(timezone.utc)
        )
        to_encode = refresh_token_payload.model_dump()
        refresh_token = cls.encode_token(to_encode)
        return refresh_token
    
    @staticmethod
    def check_password_strength(password: str) -> bool:
        if len(password) < 8 and len(password) > 22:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True
        

auth_utils = AuthUtilities()