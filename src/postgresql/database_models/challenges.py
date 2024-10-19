from postgresql.database_models.base import Base
from typing import Optional
from sqlalchemy import Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Challenges(Base):
    __tablename__ = "challenges"
    
    id:Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    title:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    video_count:Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    view_count:Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    posts = relationship("Posts", secondary="posts_challenges", back_populates="challenges")
    
    __table_args__ = (
        Index("challenges_id", "id"),
        Index("challenges_title", "title"),
    )
    
    def __repr__(self):
        return (
            f"Challenge("
            f"id={self.id}, "
            f"title={self.title!r}, "
            f"video_count={self.video_count!r}, "
            f"view_count={self.view_count!r}"
            f")"
        )