from typing import Optional

from sqlalchemy import Boolean, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Authors(Base):
    __tablename__ = "authors"

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    nickname: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    signature: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    unique_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    verified: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    posts = relationship("Posts", back_populates="authors")

    __table_args__ = (
        Index("authors_id", "id"),
        Index("authors_unique_id", "unique_id"),
    )

    def __repr__(self):
        return (
            f"Author("
            f"id={self.id}, "
            f"nickname={self.nickname!r}, "
            f"unique_id={self.unique_id!r}"
            f")"
        )
