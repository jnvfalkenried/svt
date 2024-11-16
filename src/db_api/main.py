# main.py
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy import func
from postgresql.config.db import session
from postgresql.database_models import Authors, Posts, ActiveHashtags, Challenges, Users
from postgresql.database_scripts.active_hashtags import insert_or_update_active_hashtag, get_active_hashtags

from auth import verify_token, create_access_token, hash_password, verify_password

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (change to specific URLs in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class HashtagRequest(BaseModel):
    hashtag: str

class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    roles: list

class LoignRequest(BaseModel):
    username: str
    password: str

@app.get("/authors")
async def get_authors():
    # Run a query to get all authors
    async with session() as s:
        result = await s.execute(select(Authors))
        authors = result.scalars().all()
        return authors
    
@app.get("/stats")
async def get_stats():
    # Run a query to get the number of authors
    async with session() as s:
        # Count authors
        author_count = await s.scalar(select(func.count()).select_from(Authors))
        
        # Count posts
        post_count = await s.scalar(select(func.count()).select_from(Posts))

        # Count active hashtags
        active_hashtags_count = await s.scalar(select(func.count()).select_from(ActiveHashtags))

        # Count challenges
        challenge_count = await s.scalar(select(func.count()).select_from(Challenges))
        
    return {
        "author_count": author_count,
        "post_count": post_count,
        "active_hashtags_count": active_hashtags_count,
        "challenge_count": challenge_count
    }

@app.get("/top_authors")
async def get_top_authors():
    # Run a query to get the top authors
    async with session() as s:
        result = await s.execute(
            select(Authors)
            .order_by(Authors.follower_count.desc())
            .limit(10)
        )
        authors = result.scalars().all()
        return authors
    
@app.post("/hashtag")
async def add_hashtag(hashtag_request: HashtagRequest):
    hashtag = hashtag_request.hashtag
    print(f"Attempting to add hashtag: {hashtag}")  # Debug log
    
    async with session() as s:
        try:
            uuid_str = str(uuid.uuid4())
            await insert_or_update_active_hashtag(id=uuid_str, title=hashtag, session=s)
            await s.commit()
            print(f"Successfully added hashtag: {hashtag}")  # Debug log
            return {"message": "Hashtag added successfully"}
        except Exception as e:
            await s.rollback()
            print(f"Error adding hashtag: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/hashtags")
async def get_hashtags():
    async with session() as s:
        hashtags = await get_active_hashtags(s)
        print(f"Retrieved hashtags: {hashtags}")  # Debug log
        return hashtags
    
@app.post("/register")
async def register_user(user: UserRequest):
    # Run a query to register a user
    async with session() as s:
        # Check if the user already exists
        result = await s.execute(
            select(Users)
            .where(Users.username == user.username)
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Hash the password
        user.password = hash_password(user.password)

        # Insert the user into the database
        async with s.begin():
            try:
                uuid_str = str(uuid.uuid4())
                await s.execute(
                    Authors.__table__.insert().values(
                        id=uuid_str,
                        username=user.username,
                        email=user.email,
                        password=user.password,
                        roles=user.roles
                    )
                )
                return {"message": "User registered successfully"}
            except Exception as e:
                print(f"Error in transaction, rolling back: {e}")
                await s.rollback()
                raise HTTPException(status_code=500, detail="Failed to register user")
            
    @app.post("/login")
    async def login(login_request: LoginRequest):
        # Run a query to login a user
        async with session() as s:
            # Check if the user exists
            result = await s.execute(
                select(Users)
                .where(Users.username == login_request.username)
            )
            user = result.scalars().first()

            # Verify the user
            if not user:
                raise HTTPException(status_code=400, detail="Invalid username or password")
            
            # Verify the password
            if not verify_password(login_request.password, user.password):
                raise HTTPException(status_code=400, detail="Invalid username or password")
            
            # Create JWT token
            access_token = create_access_token(data={"username": user.username, "email": user.email, "roles": user.roles})
            return {"access_token": access_token, "token_type": "bearer"}
