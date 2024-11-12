from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from sqlalchemy.schema import PrimaryKeyConstraint
from typing import Optional


class ActiveHashtags(Base):
    __tablename__ = "active_hashtags"
    
    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    
    __table_args__ = (
        PrimaryKeyConstraint("id", "active"),
    )
    
    def __repr__(self):
        return (
            f"ActiveHashtag("
            f"id={self.id}, "
            f"title={self.title!r}, "
            f"active={self.active}"
            f")"
        )