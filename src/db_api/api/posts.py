from fastapi import APIRouter, Query
from postgresql.config.db import session
from postgresql.database_scripts.posts_reporting import get_top_feed_posts, get_top_posts
from schemas.request import PostsRequest
from schemas.response import FeedResponse, PostResponse
from typing import Annotated, Union

router = APIRouter()

@router.get("/posts")
async def get_posts(request: Annotated[PostsRequest, Query()]) -> Union[list[FeedResponse], list[PostResponse]]:
    if request.feed:
        async with session() as s:
            posts = await get_top_feed_posts(
                request.start_date.replace(tzinfo=None),
                request.end_date.replace(tzinfo=None),
                request.hashtag,
                s
            )

        return posts
    else:
        async with session() as s:
            posts = await get_top_posts(
                request.start_date.replace(tzinfo=None),
                request.end_date.replace(tzinfo=None),
                request.hashtag,
                s
            )

        return posts