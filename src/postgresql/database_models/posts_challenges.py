from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PostsChallenges(Base):
    """
    A model that represents the many-to-many relationship between Posts and Challenges.
    """

    __tablename__ = "posts_challenges"

    post_id: Mapped[str] = mapped_column(
        ForeignKey("posts.id"), primary_key=True, comment="The ID of the post."
    )

    challenge_id: Mapped[str] = mapped_column(
        ForeignKey("challenges.id"), primary_key=True, comment="The ID of the challenge."
    )
