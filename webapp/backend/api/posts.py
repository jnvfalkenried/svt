from typing import Annotated, Union

from fastapi import APIRouter, Query
from schemas.request import PostsRequest
from schemas.response import ReportFeedResponse, ReportPostResponse

from postgresql.config.db import session
from postgresql.database_scripts.posts_reporting import (
    get_top_feed_posts,
    get_top_posts,
)

router = APIRouter()


@router.get("/api/posts")
async def get_posts(
    request: Annotated[PostsRequest, Query()]
) -> Union[list[ReportFeedResponse], list[ReportPostResponse]]:
    """
    Fetches top posts based on play counts within the specified date range and filters.

    Args:
        request: The request data with start_date, end_date, hashtag, category, and limit

    Returns:
        A list of dictionaries representing the top posts.
    """
    category_mapping = {
        "Views": "max_play_count",
        "Likes": "max_digg_count",
        "Comments": "max_comment_count",
        "Shares": "max_share_count",
        "Reposts": "max_repost_count",
        "Saves": "max_collect_count",
    }
    if request.feed:
        async with session() as s:
            posts = await get_top_feed_posts(
                start_date=request.start_date.replace(tzinfo=None),
                end_date=request.end_date.replace(tzinfo=None),
                hashtag=request.hashtag,
                session=s,
                limit=request.limit,
            )

        return posts
    else:
        async with session() as s:
            posts = await get_top_posts(
                start_date=request.start_date.replace(tzinfo=None),
                end_date=request.end_date.replace(tzinfo=None),
                hashtag=request.hashtag,
                category=category_mapping[request.category],
                session=s,
                limit=request.limit,
            )

        return posts
