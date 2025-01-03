from typing import Optional

from sqlalchemy import Boolean, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Music(Base):
    """
    Represents a Music object in the database.

    Attributes:
        id (str): Unique identifier for the music.
        author_name (str): The name of the author of the music.
        title (str): The title of the music.
        original (bool): Whether the music is an original work.
        duration (int): The duration of the music in seconds.
    """
    __tablename__ = "music"

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    author_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    original: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    posts = relationship("Posts", back_populates="music")

    __table_args__ = (
        # Create an index on the id column for faster lookups.
        Index("music_id", "id"),
        # Create an index on the author_name column for faster lookups.
        Index("music_author_name", "author_name"),
    )

    def __repr__(self):
        """
        Returns a string representation of the Music object.

        Returns:
            str: A string representation of the Music object.
        """
        return (
            f"Music("
            f"id={self.id}, "
            f"author_name={self.author_name!r}, "
            f"title={self.title!r}, "
            f"duration={self.duration!r}, "
            f")"
        )
