# main.py
import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy import func, text
from postgresql.config.db import session
from postgresql.database_models import Authors, Posts, ActiveHashtags, Challenges
from postgresql.database_scripts.active_hashtags import insert_or_update_active_hashtag, get_active_hashtags
from vertexai.vision_models import Image, MultiModalEmbeddingModel
import numpy as np
from typing import Optional, List, Dict, Any
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class HashtagRequest(BaseModel):
    hashtag: str

def serialize_author(author: Any) -> Dict[str, Any]:
    """Safely serialize an author object to a dictionary."""
    if not author:
        return None
    return {
        "id": str(author.id),
        "username": str(author.nickname) if author.nickname is not None else "Unknown",
        "signature": str(author.signature) if author.signature is not None else "Unknown",
        "follower_count": int(author.follower_count) if author.follower_count is not None else 0,
        "following_count": int(author.following_count) if author.following_count is not None else 0
    }

def serialize_posts(post: Any) -> Dict[str, Any]:
    """Safely serialize a post object to a dictionary."""
    if not post:
        return None
    return {
        "id": str(post.id),
        "created_at": int(post.created_at) if post.created_at is not None else None,
        "description": str(post.description) if post.description is not None else "",
        "duet_enabled": bool(post.duet_enabled) if post.duet_enabled is not None else False,
        "duet_from_id": str(post.duet_from_id) if post.duet_from_id is not None else None,
        "is_ad": bool(post.is_ad) if post.is_ad is not None else False,
        "can_repost": bool(post.can_repost) if post.can_repost is not None else False,
        "author_id": str(post.author_id) if post.author_id is not None else None,
        "music_id": str(post.music_id) if post.music_id is not None else None,
    }

def serialize_match(match: Any, author: Optional[Any] = None, post: Optional[Any] = None) -> Dict[str, Any]:
    """Safely serialize a database match to a dictionary."""
    return {
        "post_id": str(match.id),
        "description": str(match.description) if match.description else "",
        "similarity": float(match.cosine_similarity),
        "element_id": str(match.element_id),
        "author": serialize_author(author),
        "post": serialize_posts(match) 
    }

@app.get("/authors")
async def get_authors():
    async with session() as s:
        result = await s.execute(select(Authors))
        authors = result.scalars().all()
        return [serialize_author(author) for author in authors]
    
@app.get("/stats")
async def get_stats():
    async with session() as s:
        author_count = await s.scalar(select(func.count()).select_from(Authors))
        post_count = await s.scalar(select(func.count()).select_from(Posts))
        active_hashtags_count = await s.scalar(select(func.count()).select_from(ActiveHashtags))
        challenge_count = await s.scalar(select(func.count()).select_from(Challenges))
        
    return {
        "author_count": int(author_count),
        "post_count": int(post_count),
        "active_hashtags_count": int(active_hashtags_count),
        "challenge_count": int(challenge_count)
    }

@app.get("/top_authors")
async def get_top_authors():
    async with session() as s:
        result = await s.execute(
            select(Authors)
            .order_by(Authors.follower_count.desc())
            .limit(10)
        )
        authors = result.scalars().all()
        return [serialize_author(author) for author in authors]
    
@app.post("/hashtag")
async def add_hashtag(hashtag_request: HashtagRequest):
    hashtag = hashtag_request.hashtag
    print(f"Attempting to add hashtag: {hashtag}")
    
    async with session() as s:
        try:
            uuid_str = str(uuid.uuid4())
            await insert_or_update_active_hashtag(id=uuid_str, title=hashtag, session=s)
            await s.commit()
            return {"message": "Hashtag added successfully"}
        except Exception as e:
            await s.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/hashtags")
async def get_hashtags():
    async with session() as s:
        hashtags = await get_active_hashtags(s)
        return hashtags
    
@app.patch("/hashtags/{hashtag_id}/deactivate")
async def deactivate_hashtag(hashtag_id: str):
    async with session() as s:
        try:
            # Update the active status to False
            result = await s.execute(
                text("""
                    UPDATE active_hashtags 
                    SET active = false 
                    WHERE id = :hashtag_id AND active = true
                """),
                {"hashtag_id": hashtag_id}
            )
            
            await s.commit()
            
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Hashtag not found or already inactive"
                )
                
            return {"message": "Hashtag deactivated successfully"}
            
        except Exception as e:
            await s.rollback()
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/multimodal")
async def multimodal_search(
    query: str = Form(default=None),
    image: UploadFile = File(default=None),
    limit: int = 3000
):
    print(f"Received request - query: {query}, image present: {image is not None}")
    
    if not query and not image:
        raise HTTPException(
            status_code=400,
            detail="Either query text or image is required"
        )
    
    try:
        model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")
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
            try:
                if isinstance(query_embedding, np.ndarray):
                    query_embedding = query_embedding.tolist()
                
                vector_str = '[' + ','.join(str(x) for x in query_embedding) + ']'
                print(f"Vector string length: {len(vector_str)}")
                
                search_query = text("""
                SELECT 
                    p.*,
                    ve.element_id,
                    1 - (ve.embedding <=> cast(:query_vector as vector)) as cosine_similarity  -- Convert to similarity
                FROM 
                    video_embeddings ve
                    JOIN posts p ON ve.post_id = p.id
                WHERE (1 - (ve.embedding <=> cast(:query_vector as vector))) > 0.2  -- Similarity threshold
                ORDER BY cosine_similarity DESC  -- Most similar first
                LIMIT :search_limit
                """)
                
                results = await s.execute(
                    search_query,
                    {
                        "query_vector": vector_str,
                        "search_limit": limit
                    }
                )
                
                matches = results.fetchall()
                print(f"Found {len(matches)} matches")
                
                if not matches:
                    return []
                
                author_ids = [match.author_id for match in matches]
                authors_query = await s.execute(
                    text("SELECT * FROM authors WHERE id = ANY(:ids)"),
                    {"ids": author_ids}
                )
                authors_dict = {str(author.id): author for author in authors_query}
                
                formatted_results = []
                for match in matches:
                    author = authors_dict.get(str(match.author_id))
                    result = serialize_match(match, author)
                    formatted_results.append(result)
                
                return formatted_results
                
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
            
    except Exception as e:
        print(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)