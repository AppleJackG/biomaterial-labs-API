import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from dotenv import load_dotenv

load_dotenv(override=True)


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]  
    LOG_LEVEL: str

    POSTGRES_DB: str 
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str 

    @property
    def DATABASE_URL(self): 
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    TEST_POSTGRES_DB: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: str

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_POSTGRES_USER}:{self.TEST_POSTGRES_PASSWORD}@{self.TEST_POSTGRES_HOST}:{self.TEST_POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"

    SECRET_KEY: str
    PUBLIC_KEY: str
    ALGORITHM: str

    ADMIN_SECRET_KEY: str
    
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_DAYS: float = 0.007

    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    CORS_METHODS: list[str]

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()