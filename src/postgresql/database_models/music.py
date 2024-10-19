from postgresql.database_models.base import Base
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Music(Base):
    __tablename__ = "music"
    
    id:Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    author_name:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    original:Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    duration:Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    posts = relationship("Posts", back_populates="music")
    
    __table_args__ = (
        Index("music_id", "id"),
        Index("music_author_name", "author_name"),
    )

    def __repr__(self):
        return (
            f"Music("
            f"id={self.id}, "
            f"author_name={self.author_name!r}, "
            f"title={self.title!r}, "
            f"duration={self.duration!r}, "
            f")"
        )