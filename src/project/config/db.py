from project.config.settings import DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

# print(DATABASE_URL)

# Create Async Engine 
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=60,
    pool_recycle=1800,
)

# Create session factory
async_session = sessionmaker(
    bind=engine,
    class_= AsyncSession,
    expire_on_commit=False
)

# Create Async Session Generator 
@asynccontextmanager
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()    # Rollback in case of error
            print('[!] Error: ', e)
            raise e
        finally:
            await session.close()       # Close session