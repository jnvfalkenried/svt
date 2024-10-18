from project.database_models.base import Base
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Authors(Base):
    __tablename__ = "authors"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    nickname: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    signature: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unique_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    verified: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    digg_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    follower_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    following_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    heart_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    video_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    posts = relationship("Posts", back_populates="author")
    
    __table_args__ = (
        Index("authors_id", "id"),
        Index("authors_unique_id", "unique_id"),
        Index("follower_counts", "follower_count"),
    )
    
    def __repr__(self):
        return (
            f"Author("
            f"id={self.id}, "
            f"nickname={self.nickname!r}, "
            f"unique_id={self.unique_id!r}, "
            f"follower_count={self.follower_count!r}, "
            f"following_count={self.following_count!r}"
            f")"
        )