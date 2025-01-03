from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base


class ActiveHashtags(Base):
    """
    Stores the active hashtags that are currently in use.

    Columns:
        id (str): The ID of the hashtag.
        title (str): The title of the hashtag.
        active (bool): Whether the hashtag is active or not.
    """

    __tablename__ = "active_hashtags"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False)

    # __table_args__ = (
    #     PrimaryKeyConstraint("id", "active"),
    # )

    def __repr__(self) -> str:
        """
        Returns a string representation of the active hashtag.

        This string representation is useful for debugging purposes.

        Returns:
            str: The string representation of the active hashtag.
        """
        return (
            f"ActiveHashtag("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"active={self.active}"
            f")"
        )
