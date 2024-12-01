from fastapi import APIRouter, Query
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from postgresql.config.db import session
from postgresql.database_models import PostTrends
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for response
class PostTrendResponse(BaseModel):
    post_id: str
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
    start_date: Optional[datetime] = Query(None, description="Filter trends from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter trends until this date"),
    limit: int = Query(50, description="Number of records to return"),
    offset: int = Query(0, description="Number of records to skip")
) -> PostTrendsListResponse:
    async with session() as s:
        # Build base query with explicit column selection
        query = select(
            PostTrends.post_id,
            PostTrends.collected_at,
            PostTrends.current_views,
            PostTrends.daily_change,
            PostTrends.weekly_change,
            PostTrends.monthly_change,
            PostTrends.daily_growth_rate,
            PostTrends.weekly_growth_rate,
            PostTrends.monthly_growth_rate
        )
        count_query = select(func.count()).select_from(PostTrends)

        # Apply filters
        if start_date:
            query = query.where(PostTrends.collected_at >= start_date)
            count_query = count_query.where(PostTrends.collected_at >= start_date)
        if end_date:
            query = query.where(PostTrends.collected_at <= end_date)
            count_query = count_query.where(PostTrends.collected_at <= end_date)

        # Order by both weekly growth rate and current views
        query = query.order_by(
            PostTrends.weekly_growth_rate.desc(),  # First by growth rate
            PostTrends.current_views.desc()        # Then by views
        )
        
        query = query.offset(offset).limit(limit)

        # Execute queries
        total = await s.scalar(count_query)
        result = await s.execute(query)
        rows = result.all()

        # Convert tuples to Pydantic models
        trends = [
            PostTrendResponse(
                post_id=row.post_id,
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

        return PostTrendsListResponse(
            items=trends,
            total=total
        )
    
@router.post("/post-trends/refresh")
async def refresh_post_trends():
    """Endpoint to refresh the materialized view"""
    async with session() as s:
        await PostTrends.refresh_view(s)
    return {"status": "success", "message": "Post trends materialized view refreshed"}