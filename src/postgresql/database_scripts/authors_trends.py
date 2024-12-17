# In postgresql/database_scripts/author_trends.py
from datetime import datetime
from sqlalchemy import select
from postgresql.database_models import AuthorTrends

async def get_author_trends(
    start_date: datetime,
    end_date: datetime,
    session,
    author_id: str = None,
    limit: int = 100,
) -> list[dict]:
    """
    Fetches author trends data within the specified date range.
    
    :param start_date: The start date for the query range
    :param end_date: The end date for the query range
    :param session: The SQLAlchemy async session
    :param author_id: Optional author_id to filter for a specific author
    :param limit: Maximum number of records to return
    :return: List of author trends records
    """
    query = select(AuthorTrends).where(
        AuthorTrends.collected_at >= start_date,
        AuthorTrends.collected_at <= end_date
    ).order_by(AuthorTrends.collected_at.desc())
    
    if author_id:
        query = query.where(AuthorTrends.author_id == author_id)
    
    query = query.limit(limit)
    
    result = await session.execute(query)
    return result.scalars().all()