from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class AuthorResponse(BaseModel):
    """
    Response schema for author data.

    This class represents the details of an author, including their unique identifier, nickname, 
    verification status, and metrics such as follower count, following count, likes, and videos.
    """
    id: str
    """The unique identifier for the author."""
    nickname: str = Field(default="Unknown")
    """The author's nickname or display name. Defaults to "Unknown"."""
    signature: str = Field(default="Unknown")
    """A custom signature for the author. Defaults to "Unknown"."""
    unique_id: str = Field(default="Unknown")
    """A globally unique identifier for the author. Defaults to "Unknown"."""
    verified: bool = Field(default=False)
    """Indicates whether the author is verified. Defaults to False."""
    last_collected_at: datetime = Field(default=None)
    """The timestamp when the author's data was last collected."""
    max_follower_count: int = Field(default=0)
    """The maximum number of followers the author has achieved."""
    max_following_count: int = Field(default=0)
    """he maximum number of accounts the author follows."""
    max_digg_count: int = Field(default=0)
    """The maximum number of likes given by the author."""
    max_heart_count: int = Field(default=0)
    """The maximum number of likes received by the author."""
    max_video_count: int = Field(default=0)
    """The maximum number of videos the author has posted."""


class PostResponse(BaseModel):
    """
    Response schema for post data.

    This class contains information about a specific post, including its metadata, 
    engagement statistics (e.g., likes, shares), and related details. 
    """
    id: str
    """The unique identifier for the post."""
    created_at: int = Field(default=None)
    """The timestamp when the post was created."""
    description: str = Field(default="Unknown")
    """A description of the post. Defaults to "Unknown"."""
    duet_enabled: bool = Field(default=False)
    """Indicates whether duet functionality is enabled for the post."""
    duet_from_id: str = Field(default=None)
    """The ID of the post from which this post is a duet."""
    is_ad: bool = Field(default=False)
    """Indicates whether the post is an advertisement."""
    can_repost: bool = Field(default=False)
    """Indicates whether the post can be reposted."""
    author_id: str = Field(default=None)
    """The ID of the author of the post."""
    music_id: str = Field(default=None)
    """The ID of the music used in the post, if applicable."""
    max_digg_count: int = Field(default=0)
    """The maximum number of likes received by the post."""
    max_play_count: int = Field(default=0)
    """The maximum number of plays or views the post has received."""
    max_share_count: int = Field(default=0)
    """The maximum number of times the post has been shared."""
    max_collect_count: int = Field(default=0)
    """The maximum number of times the post has been collected."""


class MatchResponse(BaseModel):
    """
    Response schema for matching post data.

    This class represents the details of a post match, including the original post, its author,
    and the similarity score of the match.
    """
    post_id: str
    """The unique identifier for the post."""
    description: str = Field(default="Unknown")
    """A brief description of the post. Defaults to "Unknown"."""
    similarity: float
    """The similarity score between the two matched posts."""
    element_id: str
    """The unique identifier for the matched element."""
    author: AuthorResponse
    """The author of the matched post."""
    post: PostResponse
    """The post details of the matched post."""


class HashtagResponse(BaseModel):
    """
    Response schema for hashtag data.

    This class represents the details of a hashtag, including its unique identifier, title, 
    and whether it's currently active.
    """
    id: str
    """The unique identifier for the hashtag."""
    title: str = Field(default="Unknown")
    """The title of the hashtag. Defaults to "Unknown"."""
    active: bool = Field(default=True)
    """Indicates whether the hashtag is currently active. Defaults to True."""


class StatsResponse(BaseModel):
    """
    Response schema for platform statistics.

    This class provides various statistics about the platform, including the number of authors,
    posts, active hashtags, and challenges.
    """
    author_count: int
    """The total number of authors on the platform."""
    post_count: int
    """The total number of posts on the platform."""
    active_hashtags_count: int
    """The number of active hashtags on the platform."""
    challenge_count: int
    """The number of challenges on the platform."""


class ReportPostResponse(BaseModel):
    """
    Response schema for reported post data.

    This class provides detailed information about a reported post, including engagement metrics
    such as likes, shares, and comments, as well as information about whether the post is an advertisement.
    """
    id: str
    """The unique identifier for the post."""
    created_at: datetime
    """The timestamp when the post was created."""
    last_collected_at: datetime
    """The timestamp when the post was last collected."""
    description: str
    """A description of the post."""
    duet_enabled: bool
    """Indicates whether duet functionality is enabled for the post."""
    duet_from_id: str
    """The ID of the post from which this post is a duet."""
    is_ad: bool
    """Indicates whether the post is an advertisement."""
    can_repost: bool
    """Indicates whether the post can be reposted."""
    author_id: str
    """The ID of the post's author."""
    author_unique_id: str
    """The unique ID of the post's author."""
    max_collect_count: int
    """The maximum number of times the post has been collected."""
    max_comment_count: int
    """The maximum number of comments on the post."""
    max_digg_count: int
    """The maximum number of likes received by the post."""
    max_play_count: int
    """The maximum number of views for the post."""
    max_repost_count: int
    """The maximum number of times the post has been reposted."""
    max_share_count: int
    """The maximum number of shares the post has received."""


class ReportFeedResponse(ReportPostResponse):
    """
    Response schema for reported feed data.

    This class extends the `ReportPostResponse` schema and adds information about 
    the number of times the post appeared in feeds.
    """
    appearances_in_feed: int
    """The number of times the post has appeared in users' feeds."""


class PlatformGrowthResponse(BaseModel):
    """
    Response schema for platform growth data.

    This class represents the growth data of the platform across various categories,
    such as author growth, post growth, and challenge growth.
    """
    author_growth: list[dict]
    """A list of growth data related to authors."""
    post_growth: list[dict]
    """A list of growth data related to posts."""
    # active_hashtags_growth: list[dict]
    challenge_growth: list[dict]
    """A list of growth data related to challenges."""
    # video_embeddings_growth: list[dict]

class PostTrendResponse(BaseModel):
    """
    Response schema for post trend data.

    This class contains the trend data for a post, including the number of views,
    changes in views over time, and growth rates.
    """
    post_id: str
    """The unique identifier for the post."""
    author_name: str
    """The name of the post's author."""
    post_description: str
    """A description of the post."""
    collected_at: datetime
    """The timestamp when the trend data was collected."""
    current_views: int
    """The current number of views for the post."""
    daily_change: int
    """The daily change in views."""
    weekly_change: int
    """The weekly change in views."""
    monthly_change: int
    """The monthly change in views."""
    daily_growth_rate: float
    """The daily growth rate in views."""
    weekly_growth_rate: float
    """The weekly growth rate in views."""
    monthly_growth_rate: float
    """The monthly growth rate in views."""
    challenges: List[str]
    """A list of challenges associated with the post."""

    class Config:
        from_attributes = True


class PostTrendsListResponse(BaseModel):
    """
    Response schema for a list of post trends.

    This class contains a list of post trends, including pagination details for the response.
    """
    items: List[PostTrendResponse]
    """A list of individual post trend data."""
    total: int
    """The total number of post trends available."""

class HashtagTrendResponse(BaseModel):
    """
    Response schema for hashtag trend data.

    This class contains trend data for a hashtag, including its growth rates over 
    different time intervals.
    """
    hashtag_id: str
    """The unique identifier for the hashtag."""
    hashtag_title: str
    """The title of the hashtag."""
    daily_growth: float
    """The daily growth rate of the hashtag."""
    weekly_growth: float
    """The weekly growth rate of the hashtag."""
    monthly_growth: float
    """The monthly growth rate of the hashtag."""

    class Config:
        from_attributes = True


class HashtagTrendsListResponse(BaseModel):
    """
    Response schema for a list of hashtag trends.

    This class contains a list of hashtag trends, including pagination details for the response.
    """
    items: List[HashtagTrendResponse]
    """A list of individual hashtag trend data."""
    total: int
    """The total number of hashtag trends available."""
