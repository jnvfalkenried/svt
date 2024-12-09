from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PostsChallenges(Base):
    __tablename__ = "posts_challenges"

    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    challenge_id: Mapped[str] = mapped_column(
        ForeignKey("challenges.id"), primary_key=True
    )
