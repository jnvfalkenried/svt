import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class VideoEmbeddings(Base):
    """
    Model for storing video embeddings.

    Each video embedding is associated with a post, and has an element_id
    that is unique for that post.
    """

    __tablename__ = "video_embeddings"

    post_id = Column(
        String, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    element_id = Column(Integer, primary_key=True)
    embedding = Column(Vector(1408))

    posts = relationship("Posts", back_populates="video_embeddings")

    @classmethod
    async def find_similar(cls, session, query_embedding, limit=10):
        """
        Find the top N most similar videos to the given query embedding.

        We use cosine distance to measure similarity.

        Args:
            session: The database session to use.
            query_embedding: The embedding to compare against.
            limit: The maximum number of similar videos to return.

        Returns:
            A list of VideoEmbeddings objects, sorted by similarity.
        """
        # Using cosine distance
        stmt = (
            sa.select(cls)
            .order_by(cls.embedding.cosine_distance(query_embedding))
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
