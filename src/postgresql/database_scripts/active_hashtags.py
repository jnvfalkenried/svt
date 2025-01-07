from typing import List

from sqlalchemy import select, text

from postgresql.database_models import ActiveHashtags


async def get_active_hashtags(session) -> list:
    """Returns a list of active hashtags from the database.

    This function queries the active_hashtags table for all rows
    where the 'active' column is True, and returns a list of
    ActiveHashtags objects.

    Args:
        session: A database session

    Returns:
        A list of ActiveHashtags objects
    """
    result = await session.execute(
        select(ActiveHashtags).where(ActiveHashtags.active == True)
    )
    hashtags = result.scalars().all()
    return hashtags


async def insert_or_update_active_hashtag(id: str, title: str, session) -> None:
    # Create new hashtag instance
    """Inserts a new active hashtag into the database or updates an existing one.

    If the given hashtag ID does not exist in the database, this function
    creates a new ActiveHashtags object and adds it to the session. If the
    hashtag ID does exist, this function updates the existing object
    with the given title and sets the 'active' field to True.

    Args:
        id: The ID of the hashtag to insert or update
        title: The title of the hashtag to insert or update
        session: A database session

    Returns:
        None
    """
    new_hashtag = ActiveHashtags(id=id, title=title, active=True)

    try:
        # Add the new hashtag
        session.add(new_hashtag)

        await session.flush()
        print("Successfully flushed new hashtag")  # Debug print
    except Exception as e:
        print(f"Error in insert_or_update_active_hashtag: {e}")
        print(f"Error type: {type(e)}")
        raise e


async def fetch_related_challenges(session) -> List[dict]:
    """
    Fetches a list of active hashtags and their related hashtags from the database.

    The related hashtags are the hashtags that are on the same post as the active
    hashtag. The query joins the active_hashtags table with the challenges table
    and the posts_challenges table to get the related hashtags.

    The function returns a list of dictionaries, where each dictionary contains
    the following keys:
        - active_hashtag_id: The ID of the active hashtag
        - active_hashtag_title: The title of the active hashtag
        - related_hashtag_id: The ID of the related hashtag
        - related_hashtag_title: The title of the related hashtag

    Returns:
        List of dictionaries
    """
    query = text(
        """
        SELECT 
            c1.id AS active_hashtag_id,
            ah.title AS active_hashtag_title,
            c2.id AS related_hashtag_id,
            c2.title AS related_hashtag_title
        FROM active_hashtags ah
        JOIN challenges c1 ON ah.title = c1.title
        JOIN posts_challenges pc1 ON c1.id = pc1.challenge_id
        JOIN posts_challenges pc2 ON pc1.post_id = pc2.post_id
        JOIN challenges c2 ON pc2.challenge_id = c2.id
        WHERE ah.active = 't'
        AND c2.id != c1.id
    """
    )

    result = await session.execute(query)
    # Explicitly create dictionaries with the expected keys
    return [
        {
            "active_hashtag_id": row.active_hashtag_id,
            "active_hashtag_title": row.active_hashtag_title,
            "related_hashtag_id": row.related_hashtag_id,
            "related_hashtag_title": row.related_hashtag_title,
        }
        for row in result.fetchall()
    ]


async def fetch_related_hashtag_growth(session, active_hashtag_id: str) -> List[dict]:
    """
    Fetches the growth data of hashtags related to a given active hashtag.

    This function queries the database for posts associated with the specified
    active hashtag ID, and retrieves related hashtags, author details, and
    trends data. The data is aggregated to include information such as
    current views, changes, and growth rates over different time intervals.

    The function returns a list of dictionaries, where each dictionary contains
    the following keys:
        - active_hashtag_id: The ID of the active hashtag.
        - active_hashtag_title: The title of the active hashtag.
        - hashtag_title: A comma-separated string of related hashtag titles.
        - post_id: The ID of the post.
        - post_description: The description of the post.
        - author_unique_id: The unique ID of the post's author.
        - author_nickname: The nickname of the post's author.
        - collected_at: The timestamp of when the data was collected.
        - current_views: The current number of views of the post.
        - daily_change: The daily change in views.
        - weekly_change: The weekly change in views.
        - monthly_change: The monthly change in views.
        - daily_growth_rate: The daily growth rate of views.
        - weekly_growth_rate: The weekly growth rate of views.
        - monthly_growth_rate: The monthly growth rate of views.

    Args:
        session: A database session.
        active_hashtag_id: The ID of the active hashtag to analyze.

    Returns:
        A list of dictionaries containing growth data of related hashtags.
    """

    query = text(
        """
        WITH active_hashtag_posts AS (
        SELECT DISTINCT post_id
        FROM posts_challenges
        WHERE challenge_id = :active_hashtag_id
    ),
    related_hashtags AS (
        SELECT pc1.post_id,
            string_agg(DISTINCT c2.title, ', ') as related_titles
        FROM active_hashtag_posts ahp
        JOIN posts_challenges pc1 ON pc1.post_id = ahp.post_id
        JOIN challenges c2 ON c2.id = pc1.challenge_id
        WHERE c2.id != :active_hashtag_id
        GROUP BY pc1.post_id
    ),
    latest_trends AS (
        SELECT DISTINCT ON (post_id)
            post_id,
            collected_at,
            current_views,
            daily_change,
            weekly_change,
            monthly_change,
            daily_growth_rate,
            weekly_growth_rate,
            monthly_growth_rate
        FROM post_trends
        ORDER BY post_id, collected_at DESC
    )
    SELECT * FROM (
        SELECT DISTINCT ON (pt.post_id)
            :active_hashtag_id AS active_hashtag_id,
            c1.title AS active_hashtag_title,
            COALESCE(rh.related_titles, '') as hashtag_titles,
            pt.post_id,
            p.description AS post_description,
            a.unique_id AS author_unique_id,
            a.nickname AS author_nickname,
            pt.collected_at,
            pt.current_views,
            pt.daily_change,
            pt.weekly_change,
            pt.monthly_change,
            pt.daily_growth_rate,
            pt.weekly_growth_rate,
            pt.monthly_growth_rate
        FROM active_hashtag_posts ahp
        JOIN posts p ON p.id = ahp.post_id
        JOIN authors a ON a.id = p.author_id
        JOIN challenges c1 ON c1.id = :active_hashtag_id
        LEFT JOIN related_hashtags rh ON rh.post_id = ahp.post_id
        JOIN latest_trends pt ON pt.post_id = ahp.post_id
        ORDER BY pt.post_id, pt.collected_at DESC
    ) sub
    ORDER BY current_views DESC
    """
    )

    result = await session.execute(query, {"active_hashtag_id": active_hashtag_id})
    return [
        {
            "active_hashtag_id": row.active_hashtag_id,
            "active_hashtag_title": row.active_hashtag_title,
            "hashtag_title": row.hashtag_titles,
            "post_id": row.post_id,
            "post_description": row.post_description,
            "author_unique_id": row.author_unique_id,
            "author_nickname": row.author_nickname,
            "collected_at": row.collected_at,
            "current_views": row.current_views,
            "daily_change": row.daily_change,
            "weekly_change": row.weekly_change,
            "monthly_change": row.monthly_change,
            "daily_growth_rate": row.daily_growth_rate,
            "weekly_growth_rate": row.weekly_growth_rate,
            "monthly_growth_rate": row.monthly_growth_rate,
        }
        for row in result.fetchall()
    ]
