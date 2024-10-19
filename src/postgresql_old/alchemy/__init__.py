# src/postgresql/alchemy/__init__.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

from .models import Base
from .database import init_db

__all__ = ['Base', 'init_db', 'DATABASE_URL']