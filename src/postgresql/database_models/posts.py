from postgresql.database_models.base import Base
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Posts(Base):
    __tablename__ = "posts"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    created_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duet_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    duet_from_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_ad: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_repost: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    collect_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    digg_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    play_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    repost_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    share_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    author_id: Mapped[Optional[str]] = mapped_column(ForeignKey("authors.id"), nullable=True)
    music_id: Mapped[Optional[str]] = mapped_column(ForeignKey("music.id"), nullable=True)
    
    challenges = relationship("Challenges", secondary="posts_challenges", back_populates="posts")
    author = relationship("Author", back_populates="posts")
    music = relationship("Music", back_populates="posts")
    
    __table_args__ = (
        Index("posts_id", "id"),
        Index("posts_created_at", "created_at"),
    )
    
    def __repr__(self):
        return (
            f"Post("
            f"id={self.id}, "
            f"collect_count={self.collect_count!r}, "
            f"comment_count={self.comment_count!r}, "
            f"digg_count={self.digg_count!r}, "
            f"play_count={self.play_count!r}"
            f"repost_count={self.repost_count!r}"
            f"share_count={self.share_count!r}"
            f")"
        )