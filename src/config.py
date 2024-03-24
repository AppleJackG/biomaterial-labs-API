import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD", "DOCKER"]  

    DATABASE_URL: str
    TEST_DATABASE_URL: str
    DOCKER_DATABASE_URL: str
    
    SECRET_KEY: str
    PUBLIC_KEY: str
    ALGORITHM: str

    ADMIN_SECRET_KEY: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    CORS_METHODS: list[str]

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()