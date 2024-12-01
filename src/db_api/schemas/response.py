from pydantic import BaseModel, Field
from datetime import datetime

class AuthorResponse(BaseModel):
    id: str
    username: str = Field(default="Unknown")
    signature: str = Field(default="Unknown")
    follower_count: int = Field(default=0)
    following_count: int = Field(default=0)

class PostResponse(BaseModel):
    id: str
    created_at: int = Field(default=None)
    description: str = Field(default="Unknown")
    duet_enabled: bool = Field(default=False)
    duet_from_id: str = Field(default=None)
    is_ad: bool = Field(default=False)
    can_repost: bool = Field(default=False)
    author_id: str = Field(default=None)
    music_id: str = Field(default=None)

class MatchResponse(BaseModel):
    post_id: str
    description: str = Field(default="Unknown")
    similarity: float
    element_id: str
    author: AuthorResponse
    post: PostResponse

class HashtagResponse(BaseModel):
    id: str
    title: str = Field(default="Unknown")
    active: bool = Field(default=True)

class StatsResponse(BaseModel):
    author_count: int
    post_count: int
    active_hashtags_count: int
    challenge_count: int

class ReportPostResponse(BaseModel):
    id: str
    created_at: datetime
    last_collected_at: datetime
    description: str
    duet_enabled: bool
    duet_from_id: str
    is_ad: bool
    can_repost: bool
    author_id: str
    author_unique_id: str
    max_collect_count: int
    max_comment_count: int
    max_digg_count: int
    max_play_count: int
    max_repost_count: int
    max_share_count: int

class ReportFeedResponse(ReportPostResponse):
    appearances_in_feed: int