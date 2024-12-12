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
    Retrieve top posts based on various engagement metrics or feed appearance.

    This endpoint returns a list of top posts, either based on their appearance in the feed 
    or by a specific engagement metric (views, likes, comments, etc.). The result can be 
    filtered by a date range, hashtag, and sorted according to the specified category.

    Args:
        request (PostsRequest): The request object containing filtering criteria.

    Returns:
        Union[list[ReportFeedResponse], list[ReportPostResponse]]: A list of posts sorted
        by either their feed appearance or specific engagement metrics.

    Raises:
        HTTPException: If an error occurs while fetching the posts.
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
