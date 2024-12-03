from sqlalchemy import Column, String, Float
from .base import Base

class ChallengeTrends(Base):
    __tablename__ = 'challenge_trends'
    
    challenge_id = Column(String, primary_key=True)
    challenge_title = Column(String)
    daily_growth = Column(Float)
    weekly_growth = Column(Float)
    monthly_growth = Column(Float)
    
    # Prevent SQLAlchemy from trying to modify the view
    __mapper_args__ = {
        'primary_key': [challenge_id]
    }