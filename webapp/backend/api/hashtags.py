import uuid
from postgresql.config.db import session
from sqlalchemy.sql import text
from fastapi import APIRouter, HTTPException
from schemas.request import HashtagRequest
from schemas.response import HashtagResponse
from postgresql.database_scripts.active_hashtags import insert_or_update_active_hashtag, get_active_hashtags

router = APIRouter()

@router.post("/hashtag")
async def add_hashtag(hashtag_request: HashtagRequest) -> dict[str, str]:
    async with session() as s:
        try:
            uuid_str = str(uuid.uuid4())
            await insert_or_update_active_hashtag(id=uuid_str, title=hashtag_request.hashtag, session=s)
            await s.commit()
            return {"message": "Hashtag added successfully"}
        except Exception as e:
            await s.rollback()
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/hashtags")
async def get_hashtags() -> list[HashtagResponse]:
    async with session() as s:
        hashtags = await get_active_hashtags(s)
        return hashtags
    
@router.patch("/hashtags/{hashtag_id}/deactivate")
async def deactivate_hashtag(hashtag_id: str) -> dict[str, str]:
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
