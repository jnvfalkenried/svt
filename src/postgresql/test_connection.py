import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(os.path.dirname(src_dir))
import asyncio

# import asyncpg
from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.postgresql.db import session

load_dotenv()


async def test_sqlalchemy_connection():
    async with session() as s:
        try:
            query = await s.execute(text("SELECT version()"))
            version = query.scalar()
            print(f"Connected to PostgreSQL: {version} using SQLAlchemy")
        except SQLAlchemyError as e:
            print(f"Error connecting to PostgreSQL: {e}")


# async def test_asyncpg_connection():
#     db_url = "postgresql://postgres:postgres@localhost:5432/svt_db"
#     try:
#         conn = await asyncpg.connect(db_url)
#         print("Connected to PostgreSQL using asyncpg")

#         result = await conn.fetch("SELECT version();")
#         print(f"Connected to PostgreSQL: {result[0]['version']} using asyncpg")

#         await conn.close()  # Close the connection
#         print("Connection closed")
#     except Exception as e:
#         print(f"Error connecting to PostgreSQL using asyncpg: {e}")


if __name__ == "__main__":
    print("Testing Async SQLAlchemy connection...")
    asyncio.run(test_sqlalchemy_connection())
    # print("Testing Async asyncpg connection...")
    # asyncio.run(test_asyncpg_connection())
    print("Tests completed successfully.")
