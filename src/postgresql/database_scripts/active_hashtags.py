from sqlalchemy import select, text
from typing import List

from postgresql.database_models import ActiveHashtags


async def get_active_hashtags(session) -> list:
    result = await session.execute(
        select(ActiveHashtags).where(ActiveHashtags.active == True)
    )
    hashtags = result.scalars().all()
    return hashtags


async def insert_or_update_active_hashtag(id: str, title: str, session) -> None:
    # Create new hashtag instance
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
    query = text("""
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
    """)
    
    result = await session.execute(query)
    # Explicitly create dictionaries with the expected keys
    return [
        {
            "active_hashtag_id": row.active_hashtag_id,
            "active_hashtag_title": row.active_hashtag_title,
            "related_hashtag_id": row.related_hashtag_id,
            "related_hashtag_title": row.related_hashtag_title
        }
        for row in result.fetchall()
    ]

async def fetch_related_hashtag_growth(session, active_hashtag_id: str) -> List[dict]:
    query = text("""
        WITH related_hashtag_ids AS (
            SELECT DISTINCT c2.id as related_id, c2.title as related_title
            FROM challenges c1
            JOIN posts_challenges pc1 ON c1.id = pc1.challenge_id
            JOIN posts_challenges pc2 ON pc1.post_id = pc2.post_id
            JOIN challenges c2 ON pc2.challenge_id = c2.id
            WHERE c1.id = :active_hashtag_id
        ),
        active_hashtag_posts AS (
            -- First get all posts that have the active hashtag
            SELECT DISTINCT post_id
            FROM posts_challenges
            WHERE challenge_id = :active_hashtag_id
        ),
        distinct_posts AS (
            -- Then get related hashtags only for posts that have the active hashtag
            SELECT DISTINCT ahp.post_id
            FROM active_hashtag_posts ahp
            JOIN posts_challenges pc ON pc.post_id = ahp.post_id
            JOIN related_hashtag_ids rh ON rh.related_id = pc.challenge_id
        )
        SELECT 
            :active_hashtag_id AS active_hashtag_id,
            c1.title AS active_hashtag_title,
            string_agg(DISTINCT rh.related_title, ', ') as hashtag_titles,
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
        FROM distinct_posts dp
        JOIN posts_challenges pc ON pc.post_id = dp.post_id
        JOIN related_hashtag_ids rh ON rh.related_id = pc.challenge_id
        JOIN post_trends pt ON pt.post_id = dp.post_id
        JOIN challenges c1 ON c1.id = :active_hashtag_id
        JOIN posts p ON p.id = dp.post_id
        JOIN authors a ON a.id = p.author_id
        GROUP BY 
            c1.title,
            pt.post_id,
            p.description,
            a.unique_id,
            a.nickname,
            pt.collected_at,
            pt.current_views,
            pt.daily_change,
            pt.weekly_change,
            pt.monthly_change,
            pt.daily_growth_rate,
            pt.weekly_growth_rate,
            pt.monthly_growth_rate
        ORDER BY pt.current_views DESC
    """)
    
    result = await session.execute(query, {"active_hashtag_id": active_hashtag_id})
    return [{
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
        "monthly_growth_rate": row.monthly_growth_rate
    } for row in result.fetchall()]