# src/postgresql/alchemy/database.py
from sqlalchemy.ext.asyncio import create_async_engine
from .models import Base
from . import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables created.")