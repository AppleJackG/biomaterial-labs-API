from typing import Any
from fastapi import APIRouter, Depends, Form

from .models import User
from .schemas import UserSchema, UserCreate, UserUpdate, UserSignUp
from .service import user_service


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/signup')
async def signup(new_user: UserCreate) -> UserSchema:
    user = await user_service.add_new_user(new_user)
    return user


@user_router.get('/me', response_model=UserSchema)
async def get_current_user(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    return user


@user_router.patch('/me', response_model=UserSchema)
async def update_user(
    new_data: UserUpdate,
    user: UserSchema = Depends(user_service.get_current_user)
) -> Any:
    user = await user_service.patch_user(user.user_id, new_data)
    return user


@user_router.delete('/me', response_model=UserSchema)
async def delete_myself(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    await user_service.delete_user(user.user_id)
    return user
