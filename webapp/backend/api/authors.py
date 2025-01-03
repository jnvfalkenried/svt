from typing import Annotated, Optional

from core.auth import verify_token
from fastapi import APIRouter, Depends, Query
from schemas.request import PostsRequest
from schemas.response import AuthorResponse, AuthorTrendsResponse
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import Users
from postgresql.database_scripts.authors_reporting import get_top_authors
from postgresql.database_scripts.authors_trends import get_author_trends

router = APIRouter()


@router.get("/api/authors")
async def get_authors(
    request: Annotated[PostsRequest, Query()],
    current_user: Users = Depends(verify_token),
) -> list[AuthorResponse]:
    """
    Fetches top authors based on follower counts within the specified date range and filters.

    :param request: The request data with start_date, end_date, hashtag, category, and limit
    :param current_user: The current user object
    :return: A list of author dictionaries
    """
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
            limit=request.limit,
        )
        return result
