from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from postgresql.config.settings import DATABASE_URL

# Create an instance of the database engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_timeout=60,
    pool_recycle=1800,
)

# Create async sessionmaker bound to this engine
session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
