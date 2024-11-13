# main.py
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy import func
from postgresql.config.db import session
from postgresql.database_models import Authors, Posts, ActiveHashtags, Challenges
from postgresql.database_scripts.active_hashtags import insert_or_update_active_hashtag

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
    # Run a query to add a hashtag
    async with session() as s:
        async with s.begin():
            try:
                uuid_str = str(uuid.uuid4())
                await insert_or_update_active_hashtag(id=uuid_str, title=hashtag, session=s)
                return {"message": "Hashtag added successfully"}
            except Exception as e:
                print(f"Error in transaction, rolling back: {e}")
                await s.rollback()
                raise HTTPException(status_code=500, detail="Failed to add hashtag")
        
@app.get("/hashtags")
async def get_hashtags():
    # Run a query to get all active hashtags
    async with session() as s:
        result = await s.execute(select(ActiveHashtags))
        hashtags = result.scalars().all()
        return hashtags
