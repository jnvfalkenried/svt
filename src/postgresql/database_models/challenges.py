from postgresql.database_models.base import Base
from typing import Optional
from sqlalchemy import Integer, String, Index
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

class Challenges(Base):
    __tablename__ = "challenges"
    
    id:Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    title:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description:Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hashtag_count:Mapped[int] = mapped_column(Integer, default=1, nullable=True)
    # view_count:Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
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
            f"hashtag_count={self.hashtag_count!r} "
            # f"view_count={self.view_count!r}"
            f")"
        )
        
    '''
    Function to handle count of hashtags. 
    If a hashtag is already present in the database, it will increment its count by 1.
    If a hashtag is not present in the database, it will create a new entry with the count set to 1.
    '''
    @classmethod
    async def add_or_update(cls, 
                            session: Session,
                            challenge_id: str,
                            title: Optional[str] = None,
                            description: Optional[str] = None,
                            hashtag_count: int = 1
                            ):
        existing_challenge = await session.get(cls, challenge_id)
        if existing_challenge:
            existing_challenge.hashtag_count += 1
        else:
            new_challenge = cls(
                id=challenge_id,
                title=title,
                description=description,
                hashtag_count=hashtag_count
            )
            session.add(new_challenge)