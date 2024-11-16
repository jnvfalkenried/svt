# main.py
import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy import func
from postgresql.config.db import session
from postgresql.database_models import Authors, Posts, ActiveHashtags, Challenges
from postgresql.database_scripts.active_hashtags import insert_or_update_active_hashtag, get_active_hashtags
from vertexai.vision_models import Image, MultiModalEmbeddingModel
import numpy as np
from scipy.spatial.distance import cosine

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

@app.post("/search/multimodal")
async def multimodal_search(
    query: str = None,
    image: UploadFile = File(None),
    limit: int = 10
):
    try:
        print(f"Received search request - query: {query}, image: {image is not None}")  # Debug log
        
        # Initialize the embedding model
        model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
        
        # Generate query embedding
        query_embedding = None
        
        if query:
            print("Generating text embedding...")  # Debug log
            embeddings = model.get_embeddings(
                contextual_text=query,
                dimension=1408
            )
            query_embedding = embeddings.text_embedding
            
        if image:
            print("Processing uploaded image...")  # Debug log
            contents = await image.read()
            with open("temp_search.jpg", "wb") as f:
                f.write(contents)
                
            image_obj = Image.load_from_file("temp_search.jpg")
            embeddings = model.get_embeddings(
                image=image_obj,
                dimension=1408
            )
            query_embedding = embeddings.image_embedding
            
            import os
            os.remove("temp_search.jpg")
            
        if not query_embedding:
            raise HTTPException(status_code=400, detail="Either query text or image is required")

        print("Searching database...")  # Debug log
        async with session() as s:
            try:
                # First try a simple query to test connection
                test_query = "SELECT 1"
                await s.execute(test_query)
                
                # Now try the actual search query
                results = await s.execute(
                    """
                    SELECT p.id, p.description, p.author_id, ve.element_id, 
                           1 - (ve.embedding <=> :embedding::vector) as similarity
                    FROM video_embeddings ve
                    JOIN posts p ON ve.post_id = p.id
                    WHERE 1 - (ve.embedding <=> :embedding::vector) > 0.7
                    ORDER BY similarity DESC
                    LIMIT :limit
                    """,
                    {
                        "embedding": list(query_embedding),  # Convert numpy array to list
                        "limit": limit
                    }
                )
                
                matches = results.fetchall()
                print(f"Found {len(matches)} matches")  # Debug log
                
                if not matches:
                    return []
                
                # Get author details
                author_ids = [match.author_id for match in matches]
                authors = await s.execute(
                    select(Authors).where(Authors.id.in_(author_ids))
                )
                authors_dict = {author.id: author for author in authors.scalars()}
                
                return [{
                    "post_id": match.id,
                    "description": match.description,
                    "similarity": float(match.similarity),
                    "element_id": match.element_id,
                    "author": authors_dict[match.author_id]
                } for match in matches]
                
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")  # Debug log
                raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
            
    except Exception as e:
        print(f"Search error: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))
    
