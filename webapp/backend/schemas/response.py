from datetime import datetime

from pydantic import BaseModel, Field


class AuthorResponse(BaseModel):
    id: str
    nickname: str = Field(default="Unknown")
    signature: str = Field(default="Unknown")
    unique_id: str = Field(default="Unknown")
    verified: bool = Field(default=False)
    last_collected_at: datetime = Field(default=None)
    max_follower_count: int = Field(default=0)
    max_following_count: int = Field(default=0)
    max_digg_count: int = Field(default=0)
    max_heart_count: int = Field(default=0)
    max_video_count: int = Field(default=0)


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
    max_digg_count: int = Field(default=0)
    max_play_count: int = Field(default=0)
    max_share_count: int = Field(default=0)
    max_collect_count: int = Field(default=0)


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

class RelatedHashtagResponse(BaseModel):
    active_hashtag_id: str
    active_hashtag_title: str
    related_hashtag_id: str
    related_hashtag_title: str

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


class PlatformGrowthResponse(BaseModel):
    author_growth: list[dict]
    post_growth: list[dict]
    # active_hashtags_growth: list[dict]
    challenge_growth: list[dict]
    # video_embeddings_growth: list[dict]

class HashtagPostsResponse(BaseModel):
    related_hashtag_title: str
    post_id: str
    collected_at: datetime
    current_views: float
    daily_change: float
    weekly_change: float
    monthly_change: float
    daily_growth_percentage: float
    weekly_growth_percentage: float
    monthly_growth_percentage: float

class AuthorTrendsResponse(BaseModel):
    author_id: str
    collected_at: datetime
    current_followers: int
    current_hearts: int
    current_diggs: int
    current_videos: int
    daily_followers_change: int
    weekly_followers_change: int
    monthly_followers_change: int
    daily_followers_growth_rate: float
    weekly_followers_growth_rate: float
    monthly_followers_growth_rate: float
