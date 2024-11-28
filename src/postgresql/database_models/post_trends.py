from datetime import datetime
from typing import Optional
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class PostTrends(Base):
    __tablename__ = 'post_trends'
    
    post_id: Mapped[str] = mapped_column(String, primary_key=True)
    collected_at: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    current_views: Mapped[int] = mapped_column(Numeric)
    daily_change: Mapped[int] = mapped_column(Numeric)
    weekly_change: Mapped[int] = mapped_column(Numeric)
    monthly_change: Mapped[int] = mapped_column(Numeric)
    daily_growth_rate: Mapped[float] = mapped_column(Numeric(10,2))
    weekly_growth_rate: Mapped[float] = mapped_column(Numeric(10,2))
    monthly_growth_rate: Mapped[float] = mapped_column(Numeric(10,2))

    def __repr__(self) -> str:
        return (
            f"PostTrends("
            f"post_id={self.post_id!r}, "
            f"collected_at={self.collected_at!r}, "
            f"daily_change={self.daily_change!r}, "
            f"weekly_change={self.weekly_change!r}, "
            f"monthly_change={self.monthly_change!r})"
        )
    
    @staticmethod
    async def refresh_view(session: AsyncSession):
        """Refresh the post_trends materialized view"""
        await session.execute(text('REFRESH MATERIALIZED VIEW post_trends;'))
        await session.commit()