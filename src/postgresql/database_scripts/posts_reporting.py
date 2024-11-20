from sqlalchemy import text
from datetime import datetime


async def insert_post_stats(
    id: str,
    collected_at: datetime,
    collect_count: int,
    comment_count: int,
    digg_count: int,
    play_count: str,
    repost_count: str,
    share_count: str,
    session,
) -> None:
    await session.execute(
        text(
            """
            INSERT INTO posts_reporting (
                id, collected_at, collect_count, comment_count, digg_count, 
                play_count, repost_count, share_count
            ) 
            VALUES (
                :id, :collected_at, :collect_count, :comment_count, :digg_count, 
                :play_count, :repost_count, :share_count
            )
            ON CONFLICT (id, collected_at) DO NOTHING
            """
        ).params(
            id=id,
            collected_at=collected_at,
            collect_count=collect_count,
            comment_count=comment_count,
            digg_count=digg_count,
            play_count=play_count,
            repost_count=repost_count,
            share_count=share_count,
        )
    )
