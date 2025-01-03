from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base


class AuthorsReporting(Base):
    __tablename__ = "authors_reporting"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    collected_at: Mapped[DateTime] = mapped_column(
        DateTime, primary_key=True, default=func.now()
    )
    digg_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    follower_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    following_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    heart_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    video_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    __table_args__ = (PrimaryKeyConstraint("id", "collected_at"),)

    def __repr__(self) -> str:
        return (
            f"AuthorsReporting("
            f"id={self.id!r}, "
            f"collected_at={self.collected_at!r}, "
            f"digg_count={self.digg_count!r}, "
            f"follower_count={self.follower_count!r}, "
            f"following_count={self.following_count!r}, "
            f"heart_count={self.heart_count!r}, "
            f"video_count={self.video_count!r}"
            f")"
        )
