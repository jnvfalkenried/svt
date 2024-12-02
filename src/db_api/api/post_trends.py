from fastapi import APIRouter, Query
from sqlalchemy.future import select
from sqlalchemy import func, join
from typing import List, Optional
from datetime import datetime
from postgresql.config.db import session
from postgresql.database_models import PostTrends, Posts, Authors
from pydantic import BaseModel

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

    class Config:
        from_attributes = True

class PostTrendsListResponse(BaseModel):
    items: List[PostTrendResponse]
    total: int

@router.get("/post-trends", response_model=PostTrendsListResponse)
async def get_post_trends(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(50),
    offset: int = Query(0)
) -> PostTrendsListResponse:
    async with session() as s:
        query = select(
            PostTrends.post_id,
            PostTrends.collected_at,
            PostTrends.current_views,
            PostTrends.daily_change,
            PostTrends.weekly_change,
            PostTrends.monthly_change,
            PostTrends.daily_growth_rate,
            PostTrends.weekly_growth_rate,
            PostTrends.monthly_growth_rate,
            Authors.nickname.label('author_name'),
            Posts.description.label('post_description')
        ).select_from(PostTrends).join(
        Posts, PostTrends.post_id == Posts.id
        ).join(
            Authors, Posts.author_id == Authors.id
        )

        # Apply filters and execute query
        if start_date:
            query = query.where(PostTrends.collected_at >= start_date)
        if end_date:
            query = query.where(PostTrends.collected_at <= end_date)

        query = query.order_by(
            PostTrends.weekly_growth_rate.desc(),
            PostTrends.current_views.desc()
        ).offset(offset).limit(limit)

        result = await s.execute(query)
        rows = result.all()

        # Get total count
        count_query = select(func.count(PostTrends.post_id)).select_from(
            PostTrends
        ).join(
            Posts, PostTrends.post_id == Posts.id
        ).join(
            Authors, Posts.author_id == Authors.id
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
                monthly_growth_rate=row.monthly_growth_rate
            ) for row in rows
        ]

        return PostTrendsListResponse(items=trends, total=total)