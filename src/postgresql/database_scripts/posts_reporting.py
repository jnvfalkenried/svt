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

async def get_top_posts(
    start_date: datetime,
    end_date: datetime,
    hashtag: str,
    session,
) -> list[dict]:
    if hashtag == "all":
        query = text(
            """
            WITH posts_reporting AS (
                SELECT 
                    id,
                    MAX(collect_count) as max_collect_count,
                    MAX(comment_count) as max_comment_count,
                    MAX(digg_count) as max_digg_count,
                    MAX(play_count) as max_play_count,
                    MAX(repost_count) as max_repost_count,
                    MAX(share_count) as max_share_count
                FROM posts_reporting
                WHERE collected_at >= :start_date AND collected_at <= :end_date
                GROUP BY id
            )
            SELECT 
                posts.id,
                posts.created_at,
                posts.description,
                posts.duet_enabled,
                posts.duet_from_id,
                posts.is_ad,
                posts.can_repost,
                posts.author_id,
                posts.music_id,
                posts_reporting.max_collect_count,
                posts_reporting.max_comment_count,
                posts_reporting.max_digg_count,
                posts_reporting.max_play_count,
                posts_reporting.max_repost_count,
                posts_reporting.max_share_count
            FROM posts
            INNER JOIN posts_reporting ON posts.id = posts_reporting.id
            ORDER BY CAST(posts_reporting.max_play_count AS INTEGER) DESC
            LIMIT 10
            """
        ).params(
            start_date=start_date,
            end_date=end_date,
        )
    else:
        query = text(
            """
            WITH post_ids AS (
                SELECT
                    post_id
                FROM posts_challenges
                WHERE challenge_id = (SELECT id FROM challenges WHERE title = :hashtag)
            ),
            posts_reporting AS (
                SELECT 
                    id,
                    MAX(collect_count) as max_collect_count,
                    MAX(comment_count) as max_comment_count,
                    MAX(digg_count) as max_digg_count,
                    MAX(play_count) as max_play_count,
                    MAX(repost_count) as max_repost_count,
                    MAX(share_count) as max_share_count
                FROM posts_reporting
                WHERE collected_at >= :start_date AND collected_at <= :end_date 
                    AND id IN (SELECT post_id FROM post_ids)
                GROUP BY id
            )
            SELECT 
                posts.id,
                posts.created_at,
                posts.description,
                posts.duet_enabled,
                posts.duet_from_id,
                posts.is_ad,
                posts.can_repost,
                posts.author_id,
                posts.music_id,
                posts_reporting.max_collect_count,
                posts_reporting.max_comment_count,
                posts_reporting.max_digg_count,
                posts_reporting.max_play_count,
                posts_reporting.max_repost_count,
                posts_reporting.max_share_count
            FROM posts
            INNER JOIN posts_reporting ON posts.id = posts_reporting.id
            ORDER BY CAST(posts_reporting.max_play_count AS INTEGER) DESC
            LIMIT 10
            """
        ).params(
            hashtag=hashtag,
            start_date=start_date,
            end_date=end_date,
        )

    result = await session.execute(
        query,
    )
    return result.fetchall()

async def get_top_feed_posts(
    start_date: datetime,
    end_date: datetime,
    hashtag: str,
    session,
) -> list[dict]:
    if hashtag == "all":
        query = text(
            """
            WITH posts_reporting AS (
                SELECT 
                    id,
                    COUNT(id) as appearances_in_feed,
                    MAX(collect_count) as max_collect_count,
                    MAX(comment_count) as max_comment_count,
                    MAX(digg_count) as max_digg_count,
                    MAX(play_count) as max_play_count,
                    MAX(repost_count) as max_repost_count,
                    MAX(share_count) as max_share_count
                FROM posts_reporting
                WHERE collected_at >= :start_date AND collected_at <= :end_date
                GROUP BY id
            )
            SELECT 
                posts.id,
                posts.created_at,
                posts.description,
                posts.duet_enabled,
                posts.duet_from_id,
                posts.is_ad,
                posts.can_repost,
                posts.author_id,
                posts.music_id,
                posts_reporting.appearances_in_feed,
                posts_reporting.max_collect_count,
                posts_reporting.max_comment_count,
                posts_reporting.max_digg_count,
                posts_reporting.max_play_count,
                posts_reporting.max_repost_count,
                posts_reporting.max_share_count
            FROM posts
            INNER JOIN posts_reporting ON posts.id = posts_reporting.id
            ORDER BY CAST(posts_reporting.appearances_in_feed AS INTEGER) DESC
            LIMIT 10
            """
        ).params(
            start_date=start_date,
            end_date=end_date,
        )
    else:
        query = text(
            """
            WITH post_ids AS (
                SELECT
                    post_id
                FROM posts_challenges
                WHERE challenge_id = (SELECT id FROM challenges WHERE title = :hashtag)
            ),
            posts_reporting AS (
                SELECT 
                    id,
                    COUNT(id) as appearances_in_feed,
                    MAX(collect_count) as max_collect_count,
                    MAX(comment_count) as max_comment_count,
                    MAX(digg_count) as max_digg_count,
                    MAX(play_count) as max_play_count,
                    MAX(repost_count) as max_repost_count,
                    MAX(share_count) as max_share_count
                FROM posts_reporting
                WHERE collected_at >= :start_date AND collected_at <= :end_date 
                    AND id IN (SELECT post_id FROM post_ids)
                GROUP BY id
            )
            SELECT 
                posts.id,
                posts.created_at,
                posts.description,
                posts.duet_enabled,
                posts.duet_from_id,
                posts.is_ad,
                posts.can_repost,
                posts.author_id,
                posts.music_id,
                posts_reporting.appearances_in_feed,
                posts_reporting.max_collect_count,
                posts_reporting.max_comment_count,
                posts_reporting.max_digg_count,
                posts_reporting.max_play_count,
                posts_reporting.max_repost_count,
                posts_reporting.max_share_count
            FROM posts
            INNER JOIN posts_reporting ON posts.id = posts_reporting.id
            ORDER BY CAST(posts_reporting.appearances_in_feed AS INTEGER) DESC
            LIMIT 10
            """
        ).params(
            hashtag=hashtag,
            start_date=start_date,
            end_date=end_date,
        )

    result = await session.execute(
        query,
    )
    return result.fetchall()
