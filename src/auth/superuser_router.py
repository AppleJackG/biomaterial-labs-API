from typing import Any, Dict
from uuid import UUID
from fastapi import APIRouter, Depends

from .schemas import UserPatch, UserSchema, UserCreate
from .service import user_service


superuser_router = APIRouter(
    prefix='/superuser', 
    tags=['Super user actions'],
    dependencies=[Depends(user_service.get_current_superuser)]
)


@superuser_router.post('/signup')
async def signup(new_user: UserCreate) -> UserSchema:
    user = await user_service.add_new_user(new_user)
    return user


@superuser_router.get('/get_users_list', response_model=list[UserSchema])
async def get_users_list(offset: int = 0, limit: int = 100) -> Any:
    users = await user_service.get_users_list(offset, limit)
    return users


@superuser_router.get('/get_user/{user_id}', response_model=UserSchema)
async def get_user_by_id(user_id: UUID) -> Any:
    user = await user_service.get_user_by_id(user_id)
    return user


@superuser_router.patch('/update_user/{user_id}', response_model=UserSchema)
async def patch_user(user_id: UUID, new_values: UserPatch) -> Any:
    user = await user_service.patch_user(user_id, new_values)
    return user


@superuser_router.delete('/delete_user/{user_id}')
async def delete_user(user_id: UUID) -> dict[str, str]:
    await user_service.delete_user(user_id)
    return {
        'message': f'user {user_id} deleted'
    }
