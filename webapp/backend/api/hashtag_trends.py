from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import ChallengeTrends
from schemas.response import HashtagTrendResponse, HashtagTrendsListResponse

router = APIRouter()

@router.get("/api/hashtag-trends", response_model=HashtagTrendsListResponse)
async def get_hashtag_trends(
    min_growth: Optional[float] = Query(
        None, description="Minimum weekly growth rate filter"
    ),
    limit: int = Query(50, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
) -> HashtagTrendsListResponse:
    """
    Retrieve the top trending hashtags based on growth metrics.

    This endpoint fetches trending hashtags sorted by their weekly growth rate, 
    with optional filters for minimum growth rate and pagination options 
    (limit and offset). It returns a list of hashtags with their respective 
    growth statistics: daily, weekly, and monthly growth rates.

    Args:
        min_growth (Optional[float]): A minimum weekly growth rate to filter hashtags by. 
                                       Only hashtags with a growth rate equal to or greater 
                                       than this value will be returned.
        limit (int): The maximum number of hashtag trends to return. Defaults to 50.
        offset (int): The number of items to skip, useful for pagination. Defaults to 0.

    Returns:
        HashtagTrendsListResponse: A response object containing a list of hashtag trends, 
                                   including the total count of hashtags matching the filter.
    """
    async with session() as s:
        # Base query using the materialized view
        query = select(
            ChallengeTrends.challenge_id,
            ChallengeTrends.challenge_title,
            ChallengeTrends.daily_growth,
            ChallengeTrends.weekly_growth,
            ChallengeTrends.monthly_growth,
        ).select_from(ChallengeTrends)

        # Apply growth filter if specified
        if min_growth is not None:
            query = query.where(ChallengeTrends.weekly_growth >= min_growth)

        # Order by weekly growth rate descending
        query = (
            query.order_by(ChallengeTrends.weekly_growth.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await s.execute(query)
        rows = result.all()

        # Get total count
        count_query = select(func.count()).select_from(ChallengeTrends)
        if min_growth is not None:
            count_query = count_query.where(ChallengeTrends.weekly_growth >= min_growth)
        total = await s.scalar(count_query)

        trends = [
            HashtagTrendResponse(
                hashtag_id=row.challenge_id,
                hashtag_title="#" + row.challenge_title,
                daily_growth=row.daily_growth,
                weekly_growth=row.weekly_growth,
                monthly_growth=row.monthly_growth,
            )
            for row in rows
        ]

        return HashtagTrendsListResponse(items=trends, total=total)
