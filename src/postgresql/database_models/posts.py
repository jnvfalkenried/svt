from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    created_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    duet_enabled: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    duet_from_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_ad: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    can_repost: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    author_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("authors.id"), nullable=True
    )
    music_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("music.id"), nullable=True
    )

    challenges = relationship(
        "Challenges", secondary="posts_challenges", back_populates="posts"
    )
    authors = relationship("Authors", back_populates="posts")
    music = relationship("Music", back_populates="posts")
    video_embeddings = relationship(
        "VideoEmbeddings", back_populates="posts", cascade="all, delete-orphan"
    )
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index("posts_id", "id"),
        Index("posts_created_at", "created_at"),
    )

    def __repr__(self):
        return (
            f"Post("
            f"id={self.id}, "
            f"description={self.description!r}, "
            f"url={self.url!r}"
            f")"
        )
