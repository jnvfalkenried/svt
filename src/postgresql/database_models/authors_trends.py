from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Numeric, String, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AuthorTrends(Base):
    __tablename__ = "author_trends"

    author_id: Mapped[str] = mapped_column(String, primary_key=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    
    # Current metrics
    current_followers: Mapped[int] = mapped_column(Numeric)
    current_hearts: Mapped[int] = mapped_column(Numeric)
    current_diggs: Mapped[int] = mapped_column(Numeric)
    current_videos: Mapped[int] = mapped_column(Numeric)
    
    # Follower changes
    daily_followers_change: Mapped[int] = mapped_column(Numeric)
    weekly_followers_change: Mapped[int] = mapped_column(Numeric)
    monthly_followers_change: Mapped[int] = mapped_column(Numeric)
    
    # Heart changes
    daily_hearts_change: Mapped[int] = mapped_column(Numeric)
    weekly_hearts_change: Mapped[int] = mapped_column(Numeric)
    monthly_hearts_change: Mapped[int] = mapped_column(Numeric)
    
    # Digg changes
    daily_diggs_change: Mapped[int] = mapped_column(Numeric)
    weekly_diggs_change: Mapped[int] = mapped_column(Numeric)
    monthly_diggs_change: Mapped[int] = mapped_column(Numeric)
    
    # Video changes
    daily_videos_change: Mapped[int] = mapped_column(Numeric)
    weekly_videos_change: Mapped[int] = mapped_column(Numeric)
    monthly_videos_change: Mapped[int] = mapped_column(Numeric)
    
    # Growth rates
    daily_followers_growth_rate: Mapped[float] = mapped_column(Numeric(10, 2))
    weekly_followers_growth_rate: Mapped[float] = mapped_column(Numeric(10, 2))
    monthly_followers_growth_rate: Mapped[float] = mapped_column(Numeric(10, 2))

    def __repr__(self) -> str:
        return (
            f"AuthorTrends("
            f"author_id={self.author_id!r}, "
            f"collected_at={self.collected_at!r}, "
            f"current_followers={self.current_followers!r}, "
            f"daily_followers_change={self.daily_followers_change!r}, "
            f"weekly_followers_change={self.weekly_followers_change!r}, "
            f"monthly_followers_change={self.monthly_followers_change!r})"
        )

    @staticmethod
    async def refresh_view(session: AsyncSession):
        """Refresh the author_trends materialized view"""
        await session.execute(text("REFRESH MATERIALIZED VIEW author_trends;"))
        await session.commit()