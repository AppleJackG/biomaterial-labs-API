from typing import Any
from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse

from .models import User
from .schemas import UserSchema, UserCreate, UserUpdate, VerifyUserEmailSchema
from .service import user_service


user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/signup', response_model=UserSchema, status_code=201)
async def signup(user_data: UserCreate) -> Any:
    user = await user_service.register_new_user(user_data)
    return user


@user_router.get('/me', response_model=UserSchema)
async def get_current_user(user: UserSchema = Depends(user_service.get_current_user)) -> Any:
    return user


@user_router.post('/me/change_password', response_model=UserSchema)
async def change_password(
    user: User = Depends(user_service.get_current_user),
    old_password: str = Form(),
    new_password: str = Form()
) -> Any:
    user = await user_service.change_password(user, old_password, new_password)
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


@user_router.post('verify_email')
async def verify_user_email(data: VerifyUserEmailSchema) -> JSONResponse:
    await user_service.verify_user_email(data)
    return {
        'message': 'Email successfully verified'
    }