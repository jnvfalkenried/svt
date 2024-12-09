import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class VideoEmbeddings(Base):
    __tablename__ = "video_embeddings"

    post_id = Column(
        String, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    element_id = Column(Integer, primary_key=True)
    embedding = Column(Vector(1408))

    posts = relationship("Posts", back_populates="video_embeddings")

    # Helper method for finding similar videos
    @classmethod
    async def find_similar(cls, session, query_embedding, limit=10):
        # Using cosine distance
        stmt = (
            sa.select(cls)
            .order_by(cls.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
