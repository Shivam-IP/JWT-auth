from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

settings = Settings()