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
