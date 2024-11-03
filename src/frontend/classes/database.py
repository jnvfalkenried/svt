# database.py
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

from postgresql.database_models import Authors, Posts

load_dotenv()

class Database:
    def __init__(self):
        DATABASE_URL = (
            f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        self.engine = create_async_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine, class_=AsyncSession)

    async def get_authors(self):
        async with self.Session() as session:
            result = await session.execute(select(Authors))
            authors = result.scalars().all()
            return [{
                "id": author.id,
                "nickname": author.nickname,
                "followers": author.follower_count,
                "hearts": author.heart_count
            } for author in authors]

    async def get_videos(self):
        async with self.Session() as session:
            result = await session.execute(select(Posts))
            videos = result.scalars().all()
            return [{
                "id": video.id,
                "desc": video.description,
                "play_count": video.play_count,
                "digg_count": video.digg_count
            } for video in videos]
