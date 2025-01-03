from sqlalchemy import Column, Float, String

from .base import Base


class ChallengeTrends(Base):
    """
    A view that stores the current trends for a given hashtag.

    Columns:
        challenge_id (str): The ID of the hashtag.
        challenge_title (str): The title of the hashtag.
        daily_growth (float): The daily growth rate of the hashtag.
        weekly_growth (float): The weekly growth rate of the hashtag.
        monthly_growth (float): The monthly growth rate of the hashtag.
    """
    __tablename__ = "challenge_trends"

    challenge_id = Column(String, primary_key=True)
    challenge_title = Column(String)
    daily_growth = Column(Float)
    weekly_growth = Column(Float)
    monthly_growth = Column(Float)

    # Prevent SQLAlchemy from trying to modify the view
    __mapper_args__ = {"primary_key": [challenge_id]}

