from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import Authors, AuthorTrends

router = APIRouter()


class AuthorTrendResponse(BaseModel):
    author_id: str
    author_nickname: str
    collected_at: datetime

    # Current metrics
    current_followers: int
    current_hearts: int
    current_diggs: int
    current_videos: int

    # Changes
    daily_followers_change: int
    weekly_followers_change: int
    monthly_followers_change: int
    daily_hearts_change: int
    weekly_hearts_change: int
    monthly_hearts_change: int
    daily_diggs_change: int
    weekly_diggs_change: int
    monthly_diggs_change: int
    daily_videos_change: int
    weekly_videos_change: int
    monthly_videos_change: int

    # Growth rates
    daily_followers_growth_rate: float
    weekly_followers_growth_rate: float
    monthly_followers_growth_rate: float

    class Config:
        from_attributes = True


class AuthorTrendsListResponse(BaseModel):
    items: List[AuthorTrendResponse]
    total: int


@router.get("/api/author-trends", response_model=AuthorTrendsListResponse)
async def get_author_trends(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    author_id: Optional[str] = None,
    limit: int = Query(50),
    offset: int = Query(0),
) -> AuthorTrendsListResponse:
    async with session() as s:
        query = (
            select(
                Authors.id.label("author_id"),
                Authors.nickname.label("author_nickname"),
                AuthorTrends.collected_at,
                # Current metrics
                AuthorTrends.current_followers,
                AuthorTrends.current_hearts,
                AuthorTrends.current_diggs,
                AuthorTrends.current_videos,
                # Changes
                AuthorTrends.daily_followers_change,
                AuthorTrends.weekly_followers_change,
                AuthorTrends.monthly_followers_change,
                AuthorTrends.daily_hearts_change,
                AuthorTrends.weekly_hearts_change,
                AuthorTrends.monthly_hearts_change,
                AuthorTrends.daily_diggs_change,
                AuthorTrends.weekly_diggs_change,
                AuthorTrends.monthly_diggs_change,
                AuthorTrends.daily_videos_change,
                AuthorTrends.weekly_videos_change,
                AuthorTrends.monthly_videos_change,
                # Growth rates
                AuthorTrends.daily_followers_growth_rate,
                AuthorTrends.weekly_followers_growth_rate,
                AuthorTrends.monthly_followers_growth_rate,
            )
            .select_from(AuthorTrends)
            .join(Authors, AuthorTrends.author_id == Authors.id)
        )

        if start_date:
            query = query.where(AuthorTrends.collected_at >= start_date)
        if end_date:
            query = query.where(AuthorTrends.collected_at <= end_date)
        if author_id:
            query = query.where(Authors.id == author_id)

        query = (
            query.order_by(
                AuthorTrends.daily_followers_growth_rate.desc(),
                AuthorTrends.current_followers.desc(),
            )
            .offset(offset)
            .limit(limit)
        )

        result = await s.execute(query)
        rows = result.all()

        print(f"Query returned {len(rows)} rows")
        if rows:
            print(f"Sample row: {rows[0]}")

        count_query = (
            select(func.count(AuthorTrends.author_id))
            .select_from(AuthorTrends)
            .join(Authors, AuthorTrends.author_id == Authors.id)
        )
        if author_id:
            count_query = count_query.where(Authors.id == author_id)
        total = await s.scalar(count_query)

        trends = [
            AuthorTrendResponse(
                author_id=row.author_id,
                author_nickname=row.author_nickname,
                collected_at=row.collected_at,
                current_followers=row.current_followers,
                current_hearts=row.current_hearts,
                current_diggs=row.current_diggs,
                current_videos=row.current_videos,
                daily_followers_change=row.daily_followers_change,
                weekly_followers_change=row.weekly_followers_change,
                monthly_followers_change=row.monthly_followers_change,
                daily_hearts_change=row.daily_hearts_change,
                weekly_hearts_change=row.weekly_hearts_change,
                monthly_hearts_change=row.monthly_hearts_change,
                daily_diggs_change=row.daily_diggs_change,
                weekly_diggs_change=row.weekly_diggs_change,
                monthly_diggs_change=row.monthly_diggs_change,
                daily_videos_change=row.daily_videos_change,
                weekly_videos_change=row.weekly_videos_change,
                monthly_videos_change=row.monthly_videos_change,
                daily_followers_growth_rate=row.daily_followers_growth_rate,
                weekly_followers_growth_rate=row.weekly_followers_growth_rate,
                monthly_followers_growth_rate=row.monthly_followers_growth_rate,
            )
            for row in rows
        ]

        return AuthorTrendsListResponse(items=trends, total=total)
