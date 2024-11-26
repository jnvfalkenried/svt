from pydantic import BaseModel
from datetime import datetime

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
