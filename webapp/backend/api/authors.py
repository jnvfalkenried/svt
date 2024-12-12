from typing import Annotated

from core.auth import verify_token
from fastapi import APIRouter, Depends, Query
from schemas.request import PostsRequest
from schemas.response import AuthorResponse
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import Users
from postgresql.database_scripts.authors_reporting import get_top_authors

router = APIRouter()


@router.get("/api/authors")
async def get_authors(
    request: Annotated[PostsRequest, Query()],
    current_user: Users = Depends(verify_token),
) -> list[AuthorResponse]:
    """
    Fetch a list of top authors based on selected metrics within a specified date range.
    
    This endpoint retrieves the top authors ranked by a given category (e.g., Likes Collected, Followers, Videos, etc.) 
    within a specified date range, and returns a list of author details. 

    Args:
        request (PostsRequest): The request object containing filters such as the start and end dates,
                                 hashtag, category, and the limit for the number of authors.
        current_user (Users): The current user object, which is used for authorization and validation
                              (via token verification).

    Returns:
        list[AuthorResponse]: A list of author response objects that include author information 
                               sorted by the specified category (Likes Collected, Likes Given, Followers, etc.).
    """
    category_mapping = {
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
            category=category_mapping[request.category],
            limit=request.limit,
        )
        return result
