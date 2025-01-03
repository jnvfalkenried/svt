from typing import Optional

from sqlalchemy import Boolean, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Authors(Base):
    """
    The Authors model represents an author in the database.

    Each author is uniquely identified by their id, which is a string. The
    nickname, signature, and unique_id are additional attributes that are
    associated with an author. The verified attribute is a boolean that
    indicates whether the author is verified or not.

    The posts attribute is a relationship to the Posts model, which
    represents a list of posts associated with an author.
    """

    __tablename__ = "authors"

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    """A unique identifier for the author."""

    nickname: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    """The nickname or username of the author."""

    signature: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    """The signature or tagline of the author."""

    unique_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    """A unique identifier for the author that is used to identify the
    author across different platforms."""

    verified: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    """A boolean that indicates whether the author is verified or not."""

    posts = relationship("Posts", back_populates="authors")
    """A list of posts associated with an author."""

    __table_args__ = (
        Index("authors_id", "id"),
        Index("authors_unique_id", "unique_id"),
    )
    """
    The __table_args__ attribute is a list of additional arguments that are
    passed to the Table constructor. In this case, we are creating two
    indexes on the id and unique_id columns, which can be used to quickly
    look up authors by their id or unique_id.
    """

    def __repr__(self):
        """
        Return a string representation of the Authors object.

        This representation includes key attributes such as id, nickname, 
        and unique_id, which are useful for debugging and logging.

        Returns:
            str: A string representation of the Authors object.
        """

        return (
            f"Author("
            f"id={self.id}, "
            f"nickname={self.nickname!r}, "
            f"unique_id={self.unique_id!r}"
            f")"
        )
