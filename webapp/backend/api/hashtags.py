import uuid

from fastapi import APIRouter, HTTPException
from schemas.request import HashtagRequest
from schemas.response import HashtagResponse
from sqlalchemy.sql import text

from postgresql.config.db import session
from postgresql.database_scripts.active_hashtags import (
    get_active_hashtags,
    insert_or_update_active_hashtag,
)

router = APIRouter()


@router.post("/api/hashtag")
async def add_hashtag(hashtag_request: HashtagRequest) -> dict[str, str]:
    """
    Add a new hashtag to the active hashtags list.

    This endpoint accepts a hashtag as input and adds it to the database 
    as an active hashtag. If the hashtag already exists, it will be updated 
    with the new information. The response will confirm the success of the operation.

    Args:
        hashtag_request (HashtagRequest): The request object containing the hashtag to add.

    Returns:
        dict[str, str]: A dictionary containing a success message upon successful addition.
    
    Raises:
        HTTPException: If there is an error in processing the request, a 500 error will be returned.
    """
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
    """
    Retrieve a list of active hashtags.

    This endpoint returns all the currently active hashtags from the database. 
    It provides the hashtag title and its active status.

    Returns:
        list[HashtagResponse]: A list of active hashtags with their details.
    """
    async with session() as s:
        hashtags = await get_active_hashtags(s)
        return hashtags


@router.patch("/api/hashtags/{hashtag_id}/deactivate")
async def deactivate_hashtag(hashtag_id: str) -> dict[str, str]:
    """
    Deactivate a hashtag, making it no longer active.

    This endpoint allows deactivating a hashtag by setting its active status to False. 
    If the hashtag is already inactive or not found, it will return a 404 error. 
    Otherwise, it will return a success message.

    Args:
        hashtag_id (str): The ID of the hashtag to deactivate.

    Returns:
        dict[str, str]: A dictionary containing a success message when the hashtag is deactivated.
    
    Raises:
        HTTPException: If the hashtag is not found or already inactive, a 404 error is raised.
        HTTPException: If there is any other error, a 500 error is raised.
    """
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
