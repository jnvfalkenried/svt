from datetime import datetime

from sqlalchemy import text


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
    """
    Insert author statistics into the authors_reporting table.

    If a row with the same id and collected_at already exists, do nothing.

    Args:
        id (str): The unique identifier of the author.
        collected_at (datetime): The time when the data was collected.
        digg_count (int): The total number of diggs the author received.
        follower_count (int): The total number of followers the author has.
        following_count (int): The total number of users the author is following.
        heart_count (int): The total number of hearts the author received.
        video_count (int): The total number of videos the author has created.
        session: The database session to use for the operation.
    """
    
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


async def get_top_authors(
    start_date: datetime,
    end_date: datetime,
    session,
    hashtag: str = "all",
    category: str = "max_play_count",
    # additional_filters: Optional[dict] = None,
    limit: int = 10,
) -> list[dict]:
    """
    Fetches top authors based on follower counts within the specified date range and filters.

    :param start_date: The start date for the query range.
    :param end_date: The end date for the query range.
    :param hashtag: The hashtag to filter by, or "all" for no hashtag filtering.
    :param category: The category to sort by, e.g. "max_play_count".
    :param session: The SQLAlchemy async session for database connection.
    :param additional_filters: A dictionary of additional filters to apply.
    :param limit: The maximum number of authors to return.
    :return: A list of author dictionaries.
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
        query = """
            id IN (
                SELECT DISTINCT p.author_id
                FROM posts p
                WHERE p.id IN (
                    SELECT pc.post_id
                    FROM posts_challenges pc
                    WHERE pc.challenge_id = (
                        SELECT c.id
                        FROM challenges c
                        WHERE c.title = :hashtag
                    )
                )
            )"""
        filters.append(query)
        params["hashtag"] = hashtag

    # Add additional filters dynamically
    # if additional_filters:
    #     for key, value in additional_filters.items():
    #         filters.append(f"{key} = :{key}")
    #         params[key] = value

    # Common query
    query = text(
        f"""
        WITH authors_rep AS (
            SELECT 
                id,
                MAX(collected_at) AS last_collected_at,
                MAX(follower_count) AS max_follower_count,
                MAX(following_count) AS max_following_count,
                MAX(digg_count) AS max_digg_count,
                MAX(heart_count) AS max_heart_count,
                MAX(video_count) AS max_video_count
            FROM authors_reporting
            WHERE {" AND ".join(filters)}
            GROUP BY id
        )
        SELECT 
            authors.id,
            authors.nickname,
            authors.signature,
            authors.unique_id,
            authors.verified,
            authors_rep.last_collected_at,
            authors_rep.max_follower_count,
            authors_rep.max_following_count,
            authors_rep.max_digg_count,
            authors_rep.max_heart_count,
            authors_rep.max_video_count
        FROM authors
        INNER JOIN authors_rep ON authors.id = authors_rep.id
        ORDER BY CAST(authors_rep.{category} AS INTEGER) DESC
        LIMIT :limit
    """
    )

    # Execute query
    result = await session.execute(query.params(**params))
    return result.fetchall()
