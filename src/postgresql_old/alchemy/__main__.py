# src/postgresql/alchemy/__main__.py
import asyncio
from .database import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
    print("Database initialization complete.")