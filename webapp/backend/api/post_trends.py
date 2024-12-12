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
from schemas.response import PostTrendResponse, PostTrendsListResponse

router = APIRouter()


@router.get("/api/post-trends", response_model=PostTrendsListResponse)
async def get_post_trends(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
) -> PostTrendsListResponse:
    """
    Retrieve post trends based on growth and engagement metrics.

    This endpoint returns a list of trending posts, including various metrics like views, 
    growth rates (daily, weekly, monthly), and associated challenges. The results can be 
    filtered by a date range and support pagination through `limit` and `offset` parameters.

    Args:
        start_date (Optional[datetime]): The start date to filter the post trends by their collection date.
        end_date (Optional[datetime]): The end date to filter the post trends by their collection date.
        limit (int): The maximum number of post trends to return (default is 50).
        offset (int): The number of items to skip, used for pagination (default is 0).

    Returns:
        PostTrendsListResponse: A response object containing a list of trending posts, 
                                 along with the total count of matching records.
    
    Raises:
        HTTPException: If there's an error while processing the query, an appropriate error message is raised.
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
