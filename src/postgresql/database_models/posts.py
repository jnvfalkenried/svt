from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Posts(Base):
    """
    Represents a TikTok post.

    Attributes:
        id (str): The unique identifier of the post.
        created_at (int): The timestamp when the post was created.
        description (str): The description of the post.
        duet_enabled (bool): Whether the post allows duets.
        duet_from_id (str): The ID of the original post that this post is a duet of.
        is_ad (bool): Whether the post is an advertisement.
        can_repost (bool): Whether the post can be reposted.

        author_id (str): The ID of the author of the post.
        music_id (str): The ID of the music used in the post.

        challenges (List[Challenges]): The challenges that the post is a part of.
        authors (Authors): The author of the post.
        music (Music): The music used in the post.
        video_embeddings (List[VideoEmbeddings]): The video embeddings of the post.
        url (str): The URL of the post.
    """
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
        """
        Return a string representation of the Posts object.

        This representation includes key attributes such as id, description, and
        url, which are useful for debugging and logging.

        Returns:
            str: A string representation of the Posts object.
        """

        return (
            f"Post("
            f"id={self.id!r}, "
            f"description={self.description!r}, "
            f"url={self.url!r}"
            f")"
        )
