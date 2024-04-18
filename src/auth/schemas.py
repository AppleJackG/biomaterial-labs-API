from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class RolesEnum(str, Enum):
    student = 'student'
    teacher = 'teacher'
    admin = 'admin'


class UserSchema(UserBase):
    user_id: UUID
    username: str
    name: str
    surname: str
    role: RolesEnum
    is_active: bool
    is_verified: bool 
    is_superuser: bool 


class UserCreate(UserBase):
    username: str
    name: str
    surname: str
    role: RolesEnum
    password: str


class UserSignUp(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    role: RolesEnum | None = None


class UserPatch(UserBase):
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    role: RolesEnum | None = None
    is_active: bool | None = None
    is_verified: bool  | None = None
    is_superuser: bool  | None = None


class AccessTokenPayload(BaseModel):
    sub: str
    username: str
    exp: datetime
    iat: datetime
    access_key: str

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenPayload(BaseModel):
    sub: str
    refresh_key: str
    exp: datetime
    iat: datetime
    access_key: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

    model_config = ConfigDict(from_attributes=True)
