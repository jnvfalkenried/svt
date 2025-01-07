from typing import Optional

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base


class PostsReporting(Base):
    """
    Table to store the reporting data of posts.

    Attributes:
        id (str): The unique identifier of the post.
        collected_at (datetime): The time when the data was collected.
        collect_count (int): The number of collections of the post.
        comment_count (int): The number of comments of the post.
        digg_count (int): The number of diggs of the post.
        play_count (int): The number of plays of the post.
        repost_count (int): The number of reposts of the post.
        share_count (int): The number of shares of the post.
        url (str): The URL of the post.
    """

    __tablename__ = "posts_reporting"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    collected_at: Mapped[DateTime] = mapped_column(
        DateTime, primary_key=True, default=func.now()
    )
    collect_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    digg_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    play_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    repost_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    share_count: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    __table_args__ = (PrimaryKeyConstraint("id", "collected_at"),)

    def __repr__(self) -> str:
        """
        Return a string representation of the PostsReporting object.

        Returns:
            str: A string representation of the PostsReporting object.
        """
        return (
            f"PostsReporting("
            f"id={self.id!r}, "
            f"collected_at={self.collected_at!r}, "
            f"collect_count={self.collect_count!r}, "
            f"comment_count={self.comment_count!r}, "
            f"digg_count={self.digg_count!r}, "
            f"play_count={self.play_count!r}, "
            f"repost_count={self.repost_count!r}, "
            f"share_count={self.share_count!r}"
            f")"
        )
