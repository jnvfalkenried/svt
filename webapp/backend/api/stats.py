from typing import Annotated

from fastapi import APIRouter, Query
from schemas.request import PlatformGrowthRequest
from schemas.response import PlatformGrowthResponse, StatsResponse
from sqlalchemy import func
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import (ActiveHashtags, Authors, Challenges,
                                        Posts, VideoEmbeddings)

router = APIRouter()


@router.get("/api/stats")
async def get_stats() -> StatsResponse:
    async with session() as s:
        author_count = await s.scalar(select(func.count()).select_from(Authors))
        post_count = await s.scalar(select(func.count()).select_from(Posts))
        active_hashtags_count = await s.scalar(
            select(func.count()).select_from(ActiveHashtags)
        )
        challenge_count = await s.scalar(select(func.count()).select_from(Challenges))

    return StatsResponse(
        author_count=int(author_count),
        post_count=int(post_count),
        active_hashtags_count=int(active_hashtags_count),
        challenge_count=int(challenge_count),
    )


async def get_daily_growth(query, interval, db):
    """Helper function to calculate monthly growth for a given model."""
    stmt = (
        select(
            func.date_trunc(interval, query.inserted_at).label("interval"),
            func.count(query.id).label("count"),
        )
        .group_by("interval")
        .order_by("interval")
    )

    # Executing the query asynchronously and fetching the result
    result = await db.execute(stmt)
    return result.all()


@router.get("/api/stats/growth")
async def get_growth_stats(
    request: Annotated[PlatformGrowthRequest, Query()]
) -> PlatformGrowthResponse:
    interval_mapping = {"Day": "day", "Week": "week", "Month": "month", "Year": "year"}
    interval_format = {
        "Day": "%Y-%m-%d",
        "Week": "%Y-%W",
        "Month": "%Y-%m",
        "Year": "%Y",
    }

    print(request.interval)

    async with session() as s:
        author_growth = await get_daily_growth(
            Authors, interval_mapping[request.interval], s
        )
        post_growth = await get_daily_growth(
            Posts, interval_mapping[request.interval], s
        )
        # active_hashtags_growth = await get_daily_growth(ActiveHashtags, interval_mapping[request.interval], s)
        challenge_growth = await get_daily_growth(
            Challenges, interval_mapping[request.interval], s
        )
        # video_embeddings_growth = await get_daily_growth(VideoEmbeddings, interval_mapping[request.interval], s)

    format_growth_data = lambda data: [
        {
            "interval": entry.interval.strftime(interval_format[request.interval]),
            "count": entry.count,
        }
        for entry in data
    ]

    response_data = PlatformGrowthResponse(
        author_growth=format_growth_data(author_growth),
        post_growth=format_growth_data(post_growth),
        # active_hashtags_growth=format_growth_data(active_hashtags_growth),
        challenge_growth=format_growth_data(challenge_growth),
        # video_embeddings_growth=format_growth_data(video_embeddings_growth)
    )

    return response_data
