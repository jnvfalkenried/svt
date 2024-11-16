# main.py
import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
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
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins for development (change to specific URLs in production)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allow all headers
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Change this to True to allow credentials
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Allow all headers to be more permissive
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
    query: str = Form(default=None),
    image: UploadFile = File(default=None),
    limit: int = 10
):
    print(f"Received request - query: {query}, image present: {image is not None}")
    
    # Validate inputs
    if not query and not image:
        raise HTTPException(
            status_code=400,
            detail="Either query text or image is required"
        )
    
    try:
        # Initialize the embedding model
        model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
        
        # Generate query embedding
        query_embedding = None
        
        if query:
            print(f"Processing text query: {query}")
            embeddings = model.get_embeddings(
                contextual_text=query,
                dimension=1408
            )
            query_embedding = embeddings.text_embedding
            print("Text embedding generated successfully")
            
        if image:
            print("Processing uploaded image")
            contents = await image.read()
            with open("temp_search.jpg", "wb") as f:
                f.write(contents)
                
            image_obj = Image.load_from_file("temp_search.jpg")
            embeddings = model.get_embeddings(
                image=image_obj,
                dimension=1408
            )
            query_embedding = embeddings.image_embedding
            print("Image embedding generated successfully")
            
            import os
            os.remove("temp_search.jpg")

        if not query_embedding:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate embedding"
            )

        print("Starting database search")
        async with session() as s:
            from sqlalchemy import text
            
            try:
                # Convert numpy array to list if necessary
                if isinstance(query_embedding, np.ndarray):
                    query_embedding = query_embedding.tolist()
                
                # Convert embedding list to PostgreSQL array string format
                vector_str = '[' + ','.join(str(x) for x in query_embedding) + ']'
                print(f"Vector string length: {len(vector_str)}")
                
                # Query with the formatted vector string
                query = text("""
                    SELECT 
                        p.id,
                        p.description,
                        p.author_id,
                        ve.element_id,
                        ve.embedding <-> cast(:query_vector as vector) as distance
                    FROM 
                        video_embeddings ve
                        JOIN posts p ON ve.post_id = p.id
                    ORDER BY distance ASC
                    LIMIT :search_limit
                """)
                
                # Execute with properly formatted vector string
                results = await s.execute(
                    query,
                    {
                        "query_vector": vector_str,
                        "search_limit": limit
                    }
                )
                
                matches = results.fetchall()
                print(f"Found {len(matches)} matches")
                
                if not matches:
                    return []
                
                # Get author details
                author_ids = [match.author_id for match in matches]
                authors = await s.execute(
                    text("SELECT * FROM authors WHERE id = ANY(:ids)"),
                    {"ids": author_ids}
                )
                authors_dict = {author.id: author for author in authors}
                
                return [{
                    "post_id": match.id,
                    "description": match.description,
                    "distance": float(match.distance),
                    "element_id": match.element_id,
                    "author": authors_dict.get(match.author_id)
                } for match in matches]
                
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
            
    except Exception as e:
        print(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))