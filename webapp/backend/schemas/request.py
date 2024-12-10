from datetime import datetime

from pydantic import BaseModel


class HashtagRequest(BaseModel):
    hashtag: str


class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    roles: str


class LoginRequest(BaseModel):
    username: str
    password: str


class PostsRequest(BaseModel):
    feed: bool
    start_date: datetime
    end_date: datetime
    hashtag: str
    category: str
    limit: int


class PlatformGrowthRequest(BaseModel):
    interval: str
