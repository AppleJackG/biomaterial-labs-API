from typing import Any
from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .schemas import Token, UserSchema
from .service import user_service, auth_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

auth_router = APIRouter(prefix='/auth', tags=['JWT Auth'])


@auth_router.post('/login', response_model=Token)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends()
) -> Any:
    token = await auth_service.login(credentials.username, credentials.password)
    return token


@auth_router.post('/refresh', response_model=Token)
async def refresh_token(refresh_token: str = Header()):
    token = await auth_service.refresh_token(refresh_token)
    return token


@auth_router.post('/logout')
async def logout(user: UserSchema = Depends(user_service.get_current_user)) -> JSONResponse:
    await auth_service.logout(user)
    return {
        'message': 'successful logout'
    }