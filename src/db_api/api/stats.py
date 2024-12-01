from fastapi import APIRouter
from sqlalchemy.future import select
from sqlalchemy import func, text
from postgresql.config.db import session
from postgresql.database_models import Authors, Posts, ActiveHashtags, Challenges, PostsReporting
from schemas.response import StatsResponse
from datetime import datetime

router = APIRouter()

@router.get("/stats")
async def get_stats() -> StatsResponse:
    async with session() as s:
        author_count = await s.scalar(select(func.count()).select_from(Authors))
        post_count = await s.scalar(select(func.count()).select_from(Posts))
        active_hashtags_count = await s.scalar(select(func.count()).select_from(ActiveHashtags))
        challenge_count = await s.scalar(select(func.count()).select_from(Challenges))
        
    return StatsResponse(
        author_count=int(author_count),
        post_count=int(post_count),
        active_hashtags_count=int(active_hashtags_count),
        challenge_count=int(challenge_count)
    )
