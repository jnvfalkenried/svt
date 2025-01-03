from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import func, join
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import (
    Authors,
    Challenges,
    Posts,
    PostsChallenges,
    PostTrends,
)

router = APIRouter()


class PostTrendResponse(BaseModel):
    post_id: str
    author_name: str
    post_description: str
    collected_at: datetime
    current_views: int
    daily_change: int
    weekly_change: int
    monthly_change: int
    daily_growth_rate: float
    weekly_growth_rate: float
    monthly_growth_rate: float
    challenges: List[str]

    class Config:
        from_attributes = True


class PostTrendsListResponse(BaseModel):
    items: List[PostTrendResponse]
    total: int


@router.get("/api/post-trends", response_model=PostTrendsListResponse)
async def get_post_trends(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
) -> PostTrendsListResponse:
    """
    Fetches post trends data within the specified date range.

    Args:
        start_date: The start date for the query range
        end_date: The end date for the query range
        limit: Maximum number of records to return
        offset: Number of records to skip

    Returns:
        PostTrendsListResponse: A response containing the list of post trends and total count
    """
    async with session() as s:
        query = (
            select(
                PostTrends.post_id,
                PostTrends.collected_at,
                PostTrends.current_views,
                PostTrends.daily_change,
                PostTrends.weekly_change,
                PostTrends.monthly_change,
                PostTrends.daily_growth_rate,
                PostTrends.weekly_growth_rate,
                PostTrends.monthly_growth_rate,
                func.array_agg(Challenges.title).label("challenges"),
                Authors.nickname.label("author_name"),
                Posts.description.label("post_description"),
            )
            .select_from(PostTrends)
            .join(Posts, PostTrends.post_id == Posts.id)
            .join(Authors, Posts.author_id == Authors.id)
            .join(PostsChallenges, Posts.id == PostsChallenges.post_id)
            .join(Challenges, PostsChallenges.challenge_id == Challenges.id)
        )

        # Apply filters and execute query
        if start_date:
            query = query.where(PostTrends.collected_at >= start_date)
        if end_date:
            query = query.where(PostTrends.collected_at <= end_date)

        query = (
            query.group_by(
                PostTrends.post_id,
                PostTrends.collected_at,
                PostTrends.current_views,
                PostTrends.daily_change,
                PostTrends.weekly_change,
                PostTrends.monthly_change,
                PostTrends.daily_growth_rate,
                PostTrends.weekly_growth_rate,
                PostTrends.monthly_growth_rate,
                Authors.nickname,
                Posts.description,
            )
            .order_by(
                PostTrends.weekly_growth_rate.desc(), PostTrends.current_views.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        result = await s.execute(query)
        rows = result.all()

        # Get total count
        count_query = (
            select(func.count(PostTrends.post_id))
            .select_from(PostTrends)
            .join(Posts, PostTrends.post_id == Posts.id)
            .join(Authors, Posts.author_id == Authors.id)
        )
        total = await s.scalar(count_query)

        trends = [
            PostTrendResponse(
                post_id=row.post_id,
                author_name=row.author_name,
                post_description=row.post_description,
                collected_at=row.collected_at,
                current_views=row.current_views,
                daily_change=row.daily_change,
                weekly_change=row.weekly_change,
                monthly_change=row.monthly_change,
                daily_growth_rate=row.daily_growth_rate,
                weekly_growth_rate=row.weekly_growth_rate,
                monthly_growth_rate=row.monthly_growth_rate,
                challenges=(
                    ["#" + challenge for challenge in row.challenges]
                    if row.challenges
                    else []
                ),
            )
            for row in rows
        ]

        return PostTrendsListResponse(items=trends, total=total)
