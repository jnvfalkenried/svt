import uuid

from fastapi import APIRouter, HTTPException
from schemas.request import HashtagRequest
from schemas.response import HashtagResponse
from sqlalchemy.sql import text

from typing import List
from schemas.response import RelatedHashtagResponse, HashtagPostsResponse


from postgresql.config.db import session
from postgresql.database_scripts.active_hashtags import (
    get_active_hashtags,
    insert_or_update_active_hashtag,
    fetch_related_challenges,
    fetch_related_hashtag_growth,
)

router = APIRouter()


@router.post("/api/hashtag")
async def add_hashtag(hashtag_request: HashtagRequest) -> dict[str, str]:
    async with session() as s:
        try:
            uuid_str = str(uuid.uuid4())
            await insert_or_update_active_hashtag(
                id=uuid_str, title=hashtag_request.hashtag, session=s
            )
            await s.commit()
            return {"message": "Hashtag added successfully"}
        except Exception as e:
            await s.rollback()
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/hashtags")
async def get_hashtags() -> list[HashtagResponse]:
    async with session() as s:
        hashtags = await get_active_hashtags(s)
        return hashtags


@router.patch("/api/hashtags/{hashtag_id}/deactivate")
async def deactivate_hashtag(hashtag_id: str) -> dict[str, str]:
    async with session() as s:
        try:
            # Update the active status to False
            result = await s.execute(
                text(
                    """
                    UPDATE active_hashtags 
                    SET active = false 
                    WHERE id = :hashtag_id AND active = true
                """
                ),
                {"hashtag_id": hashtag_id},
            )

            await s.commit()

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Hashtag not found or already inactive"
                )

            return {"message": "Hashtag deactivated successfully"}

        except Exception as e:
            await s.rollback()
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/hashtags/related", response_model=List[RelatedHashtagResponse])
async def get_related_hashtags() -> List[RelatedHashtagResponse]:
    async with session() as s:
        try:
            results = await fetch_related_challenges(s)
            print("Debug - Fetched results:", results)  # Debug print
            return results
        except Exception as e:
            print("Debug - Error:", str(e))  # Debug print
            raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/api/hashtags/{active_hashtag}/trends")
async def get_related_hashtag_trends(active_hashtag: str):
    async with session() as s:
        try:
            results = await fetch_related_hashtag_growth(s, active_hashtag)
            if not results:
                raise HTTPException(
                    status_code=404,
                    detail=f"No trends found for hashtags related to #{active_hashtag}"
                )
            return results
        except Exception as e:
            print("Debug - Error:", str(e))
            raise HTTPException(status_code=500, detail=str(e))
