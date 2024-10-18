#### THIS STEP IS ONLY REQUIRED IN WINDOWS #####
import os
from dotenv import load_dotenv
load_dotenv()
PROJECT_PATH = os.getenv("PROJECT_PATH")
import sys
sys.path.append(PROJECT_PATH)
################################################
from project.config.settings import DATABASE_URL
from project.config.db import get_async_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import asyncpg
import asyncio

print(DATABASE_URL)

async def test_sqlalchemy_connection():
    async with get_async_session() as session:
        try:
            result = await session.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"Connected to PostgreSQL: {version} using SQLAlchemy")
        except SQLAlchemyError as e:
            print(f"Error connecting to PostgreSQL: {e}")

async def test_asyncpg_connection():
    db_url = "postgresql://postgres:postgres@localhost:5432/svt_db"
    try:
        conn = await asyncpg.connect(db_url)
        print("Connected to PostgreSQL using asyncpg")
        
        result = await conn.fetch("SELECT version();")
        print(f"Connected to PostgreSQL: {result[0]['version']} using asyncpg")
        
        await conn.close()  # Close the connection
        print("Connection closed")
    except Exception as e:
        print(f"Error connecting to PostgreSQL using asyncpg: {e}")

if __name__ == "__main__":
    print("Testing Async SQLAlchemy connection...")
    asyncio.run(test_sqlalchemy_connection())
    print("Testing Async asyncpg connection...")
    asyncio.run(test_asyncpg_connection())
    print("Tests completed successfully.")