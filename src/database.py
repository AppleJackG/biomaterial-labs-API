from sqlalchemy import NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import settings


if settings.MODE == 'DEV':
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}
elif settings.MODE == 'TEST':
    SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
elif settings.MODE == 'DOCKER_TEST':
    SQLALCHEMY_DATABASE_URL = settings.DOCKER_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
elif settings.MODE == 'PROD':
    SQLALCHEMY_DATABASE_URL = settings.DOCKER_DATABASE_URL
    DATABASE_PARAMS = {}
else:
    raise ValueError(f"Unknown mode: {settings.MODE}")


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, **DATABASE_PARAMS)


session_factory = async_sessionmaker(autoflush=False, autocommit=False, bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
