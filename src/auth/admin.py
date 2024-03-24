from fastapi import Request
from sqladmin.authentication import AuthenticationBackend
from .service import user_service, auth_service
from ..config import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        await user_service.check_admin_rights(username, password)
        tokens = await auth_service.login(username, password)
        request.session.update({"token": tokens.access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True
    

authentication_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)