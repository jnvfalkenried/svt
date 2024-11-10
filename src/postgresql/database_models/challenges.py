from typing import Optional

from database_models.base import Base
from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Challenges(Base):
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

    def __repr__(self):
        return (
            f"Challenge("
            f"id={self.id}, "
            f"title={self.title!r}, "
            f"hashtag_count={self.hashtag_count!r}"
            f")"
        )
