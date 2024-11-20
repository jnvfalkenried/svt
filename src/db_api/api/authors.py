from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from postgresql.database_models import Authors, Users
from postgresql.config.db import session
from core.auth import verify_token

from schemas.response import AuthorResponse

router = APIRouter()


@router.get("/authors")
async def get_authors(current_user: Users = Depends(verify_token)) -> list[AuthorResponse]:
    async with session() as s:
        result = await s.execute(select(Authors))
        authors = result.scalars().all()
        return authors
    
@router.get("/top_authors")
async def get_top_authors(current_user: Users = Depends(verify_token)) -> list[AuthorResponse]:
    # Run a query to get the top authors
    async with session() as s:
        result = await s.execute(
            select(Authors)
            .order_by(Authors.follower_count.desc())
            .limit(10)
        )
        authors = result.scalars().all()
        return authors