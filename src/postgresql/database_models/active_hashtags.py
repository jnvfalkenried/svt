from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint

from .base import Base


class ActiveHashtags(Base):
    __tablename__ = "active_hashtags"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False)

    # __table_args__ = (
    #     PrimaryKeyConstraint("id", "active"),
    # )

    def __repr__(self):
        return (
            f"ActiveHashtag("
            f"id={self.id}, "
            f"title={self.title!r}, "
            f"active={self.active}"
            f")"
        )
