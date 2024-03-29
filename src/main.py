from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from .auth.models import UserAdmin, RefreshTokenAdmin
from .config import settings
from .auth.auth_router import auth_router
from .auth.user_router import user_router
from .auth.superuser_router import superuser_router
from .auth.admin import authentication_backend
from .database import engine
from .labs.main_labs_router import router_labs


app = FastAPI(title="Template")
admin = Admin(app, engine, authentication_backend=authentication_backend)


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(superuser_router)
app.include_router(router_labs)

admin.add_view(UserAdmin)
admin.add_view(RefreshTokenAdmin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/", response_class=HTMLResponse)
async def home():
    if settings.MODE == 'PROD':
        main_page = (
            '<p>Welcome to FastAPI template. v.0.1.0</p>'
        )
    else:
        main_page = (
            f'<a href="/docs">Documentation</a><br>'
            f'<a href="/redoc">ReDoc</a>'
        )
    return main_page
