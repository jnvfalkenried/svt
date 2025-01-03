from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import ChallengeTrends

router = APIRouter()


class HashtagTrendResponse(BaseModel):
    hashtag_id: str
    hashtag_title: str
    daily_growth: float
    weekly_growth: float
    monthly_growth: float

    class Config:
        from_attributes = True


class HashtagTrendsListResponse(BaseModel):
    items: List[HashtagTrendResponse]
    total: int


@router.get("/api/hashtag-trends", response_model=HashtagTrendsListResponse)
async def get_hashtag_trends(
    min_growth: Optional[float] = Query(
        None, description="Minimum weekly growth rate filter"
    ),
    limit: int = Query(50, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
) -> HashtagTrendsListResponse:
    """
    Fetches a list of hashtag trends, sorted by weekly growth rate descending.

    Args:
        min_growth: Optional minimum weekly growth rate filter. If specified,
            only hashtags with a weekly growth rate greater than or equal to
            this value will be returned.
        limit: Number of items to return. Defaults to 50.
        offset: Number of items to skip. Defaults to 0.

    Returns:
        A list of HashtagTrendResponse objects, containing the hashtag ID,
        hashtag title (with '#' prefix), daily growth rate, weekly growth rate,
        and monthly growth rate. The list is sorted by weekly growth rate
        descending. The total count is also returned.
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
