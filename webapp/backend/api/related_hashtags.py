from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.future import select

from postgresql.config.db import session
from postgresql.database_models import RelatedHashtags

router = APIRouter()


class RelatedHashtagRequest(BaseModel):
    hashtags: List[str]
    related_hashtags: List[str]
    support: float
    confidence: float
    lift: float

    class Config:
        from_attributes = True


class RelatedHashtagListResponse(BaseModel):
    related_hashtag_rules: List[RelatedHashtagRequest]
    total: int


@router.get("/api/related-hashtags", response_model=RelatedHashtagListResponse)
async def get_related_hashtags(
    min_support: Optional[float] = Query(None, description="Minimum support filter"),
    limit: int = Query(50, description="Number of items to return"),
    offset: int = Query(0, description="Number of items to skip"),
) -> RelatedHashtagListResponse:
    async with session() as s:
        # Base query using the materialized view
        query = (
            select(
                RelatedHashtags.antecedent_title.label("hashtags"),
                RelatedHashtags.consequent_title.label("related_hashtags"),
                RelatedHashtags.support,
                RelatedHashtags.confidence,
                RelatedHashtags.lift,
            )
            .select_from(RelatedHashtags)
            .order_by(RelatedHashtags.support.desc())
            .offset(offset)
            .limit(limit)
        )

        count_query = select(func.count()).select_from(RelatedHashtags)

        # Apply support filter if specified
        if min_support is not None:
            query = query.where(RelatedHashtags.support >= min_support)
            count_query = count_query.where(RelatedHashtags.support >= min_support)

        result = await s.execute(query)
        total_rows = await s.execute(count_query)

        total = total_rows.scalar()

        related_hashtag_rules = [
            RelatedHashtagRequest(
                hashtags=[f"#{tag}" for tag in row.hashtags],
                related_hashtags=[f"#{tag}" for tag in row.related_hashtags],
                support=row.support,
                confidence=row.confidence,
                lift=row.lift,
            )
            for row in result
        ]

        return RelatedHashtagListResponse(
            related_hashtag_rules=related_hashtag_rules, total=total
        )
