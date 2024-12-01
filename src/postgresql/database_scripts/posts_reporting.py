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
    session,
    hashtag: str = "all",
    category: str = "max_play_count",
    # additional_filters: Optional[dict] = None,
    limit: int = 10
) -> list[dict]:
    """
    Fetches top posts based on play counts within the specified date range and filters.

    :param start_date: The start date for the query range.
    :param end_date: The end date for the query range.
    :param hashtag: The hashtag to filter by, or "all" for no hashtag filtering.
    :param category: The category to sort by, e.g. "max_play_count".
    :param session: The SQLAlchemy async session for database connection.
    :param additional_filters: A dictionary of additional filters to apply.
    :param limit: The maximum number of posts to return.
    :return: A list of dictionaries representing the top posts.
    """
    
    # Base query components
    filters = ["collected_at >= :start_date", "collected_at <= :end_date"]
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
    }

    # Add hashtag-specific filtering
    if hashtag != "all":
        filters.append("id IN (SELECT post_id FROM posts_challenges WHERE challenge_id = (SELECT id FROM challenges WHERE title = :hashtag))")
        params["hashtag"] = hashtag

    # Add additional filters dynamically
    # if additional_filters:
    #     for key, value in additional_filters.items():
    #         filters.append(f"{key} = :{key}")
    #         params[key] = value

    # Common query
    query = text(f"""
        WITH posts_reporting AS (
            SELECT 
                id,
                MAX(collected_at) AS last_collected_at,
                MAX(collect_count) AS max_collect_count,
                MAX(comment_count) AS max_comment_count,
                MAX(digg_count) AS max_digg_count,
                MAX(play_count) AS max_play_count,
                MAX(repost_count) AS max_repost_count,
                MAX(share_count) AS max_share_count
            FROM posts_reporting
            WHERE {" AND ".join(filters)}
            GROUP BY id
        )
        SELECT 
            posts.id,
            posts.created_at,
            posts_reporting.last_collected_at,
            posts.description,
            posts.duet_enabled,
            posts.duet_from_id,
            posts.is_ad,
            posts.can_repost,
            posts.author_id,
            authors.unique_id AS author_unique_id,
            posts_reporting.max_collect_count,
            posts_reporting.max_comment_count,
            posts_reporting.max_digg_count,
            posts_reporting.max_play_count,
            posts_reporting.max_repost_count,
            posts_reporting.max_share_count
        FROM posts
        INNER JOIN posts_reporting ON posts.id = posts_reporting.id
        LEFT JOIN authors ON posts.author_id = authors.id
        ORDER BY CAST(posts_reporting.{category} AS INTEGER) DESC
        LIMIT :limit
    """)

    # Execute query
    result = await session.execute(query.params(**params))
    return result.fetchall()

async def get_top_feed_posts(
    start_date: datetime,
    end_date: datetime,
    session,
    hashtag: str = "all",
    # additional_filters: Optional[dict] = None,
    limit: int = 10
) -> list[dict]:
    """
    Fetches top feed posts based on appearances in feed within the specified date range and filters.

    :param start_date: The start date for the query range.
    :param end_date: The end date for the query range.
    :param hashtag: The hashtag to filter by, or "all" for no hashtag filtering.
    :param session: The SQLAlchemy async session for database connection.
    :param additional_filters: A dictionary of additional filters to apply.
    :param limit: The maximum number of posts to return.
    :return: A list of dictionaries representing the top feed posts.
    """
    # Base filters and parameters
    filters = ["collected_at >= :start_date", "collected_at <= :end_date"]
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
    }

    # Add hashtag-specific filtering
    if hashtag != "all":
        filters.append("id IN (SELECT post_id FROM posts_challenges WHERE challenge_id = (SELECT id FROM challenges WHERE title = :hashtag))")
        params["hashtag"] = hashtag

    # Add additional filters dynamically
    # if additional_filters:
    #     for key, value in additional_filters.items():
    #         filters.append(f"{key} = :{key}")
    #         params[key] = value

    # Construct the query dynamically
    query = text(f"""
        WITH posts_reporting AS (
            SELECT 
                id,
                MAX(collected_at) AS last_collected_at,
                COUNT(id) AS appearances_in_feed,
                MAX(collect_count) AS max_collect_count,
                MAX(comment_count) AS max_comment_count,
                MAX(digg_count) AS max_digg_count,
                MAX(play_count) AS max_play_count,
                MAX(repost_count) AS max_repost_count,
                MAX(share_count) AS max_share_count
            FROM posts_reporting
            WHERE {" AND ".join(filters)}
            GROUP BY id
        )
        SELECT 
            posts.id,
            posts.created_at,
            posts_reporting.last_collected_at,
            posts.description,
            posts.duet_enabled,
            posts.duet_from_id,
            posts.is_ad,
            posts.can_repost,
            posts.author_id,
            authors.unique_id AS author_unique_id,
            posts_reporting.appearances_in_feed,
            posts_reporting.max_collect_count,
            posts_reporting.max_comment_count,
            posts_reporting.max_digg_count,
            posts_reporting.max_play_count,
            posts_reporting.max_repost_count,
            posts_reporting.max_share_count
        FROM posts
        INNER JOIN posts_reporting ON posts.id = posts_reporting.id
        LEFT JOIN authors ON posts.author_id = authors.id
        ORDER BY CAST(posts_reporting.appearances_in_feed AS INTEGER) DESC
        LIMIT :limit
    """)

    # Execute the query
    result = await session.execute(query.params(**params))

    return result.fetchall()
