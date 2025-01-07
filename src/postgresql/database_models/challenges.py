from typing import Optional

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Challenges(Base):
    """
    The Challenges model represents a hashtag challenge in the database.

    Each challenge is uniquely identified by their id, which is a string. The
    title, description, and hashtag_count are additional attributes that are
    associated with a challenge. The posts attribute is a relationship to the
    Posts model, which represents a list of posts associated with an author.
    """

    __tablename__ = "challenges"

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hashtag_count: Mapped[int] = mapped_column(Integer, default=1, nullable=True)

    posts = relationship(
        "Posts", secondary="posts_challenges", back_populates="challenges"
    )

    __table_args__ = (
        Index("challenges_id", "id"),
        Index("challenges_title", "title"),
    )

    def __repr__(self) -> str:
        """
        Return a string representation of the Challenges object.

        This representation includes key attributes such as id, title, and
        hashtag_count, which are useful for debugging and logging.

        Returns:
            str: A string representation of the Challenges object.
        """
        return (
            f"Challenge("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"hashtag_count={self.hashtag_count!r}"
            f")"
        )
