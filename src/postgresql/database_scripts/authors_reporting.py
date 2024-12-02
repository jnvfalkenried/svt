from sqlalchemy import text
from datetime import datetime


async def insert_author_stats(
    id: str,
    collected_at: datetime,
    digg_count: int,
    follower_count: int,
    following_count: int,
    heart_count: int,
    video_count: int,
    session,
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO authors_reporting (
                id, collected_at, digg_count, follower_count, 
                following_count, heart_count, video_count
            ) 
            VALUES (
                :id, :collected_at, :digg_count, :follower_count,
                :following_count, :heart_count, :video_count
            )
            ON CONFLICT (id, collected_at) DO NOTHING
            """
        ).params(
            id=id,
            collected_at=collected_at,
            digg_count=digg_count,
            follower_count=follower_count,
            following_count=following_count,
            heart_count=heart_count,
            video_count=video_count,
        )
    )
