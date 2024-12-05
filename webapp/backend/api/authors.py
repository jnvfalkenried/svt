from fastapi import APIRouter, Depends, Query
from sqlalchemy.future import select
from postgresql.database_models import Users
from postgresql.database_scripts.authors_reporting import get_top_authors
from postgresql.config.db import session
from core.auth import verify_token
from schemas.request import PostsRequest
from typing import Annotated

from schemas.response import AuthorResponse

router = APIRouter()


@router.get("/authors")
async def get_authors(request: Annotated[PostsRequest, Query()], current_user: Users = Depends(verify_token)) -> list[AuthorResponse]:
    hashtag_mapping = {
        "Likes Collected": "max_heart_count",
        "Likes Given": "max_digg_count",
        "Followers": "max_follower_count",
        "Following": "max_following_count",
        "Videos": "max_video_count",
    }
    
    async with session() as s:
        result = await get_top_authors(
            start_date=request.start_date.replace(tzinfo=None),
            end_date=request.end_date.replace(tzinfo=None),
            session=s,
            hashtag=request.hashtag,
            category=hashtag_mapping[request.category],
            limit=request.limit
        )
        return result
