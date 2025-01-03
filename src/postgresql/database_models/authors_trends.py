from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Numeric, String, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AuthorTrends(Base):
    """
    Table to store trends for authors.

    See https://www.postgresql.org/docs/current/rules-materializedviews.html
    """
    __tablename__ = "author_trends"

    author_id: Mapped[str] = mapped_column(String, primary_key=True)
    """
    Unique identifier of the author.
    """
    collected_at: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    """
    Timestamp when the trends were collected.
    """

    # Current metrics
    current_followers: Mapped[int] = mapped_column(Numeric)
    """
    Number of followers the author currently has.
    """
    current_hearts: Mapped[int] = mapped_column(Numeric)
    """
    Number of hearts the author currently has.
    """
    current_diggs: Mapped[int] = mapped_column(Numeric)
    """
    Number of diggs the author currently has.
    """
    current_videos: Mapped[int] = mapped_column(Numeric)
    """
    Number of videos the author currently has.
    """

    # Follower changes
    daily_followers_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of followers the author gained in the last day.
    """
    weekly_followers_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of followers the author gained in the last week.
    """
    monthly_followers_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of followers the author gained in the last month.
    """

    # Heart changes
    daily_hearts_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of hearts the author gained in the last day.
    """
    weekly_hearts_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of hearts the author gained in the last week.
    """
    monthly_hearts_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of hearts the author gained in the last month.
    """

    # Digg changes
    daily_diggs_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of diggs the author gained in the last day.
    """
    weekly_diggs_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of diggs the author gained in the last week.
    """
    monthly_diggs_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of diggs the author gained in the last month.
    """

    # Video changes
    daily_videos_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of videos the author gained in the last day.
    """
    weekly_videos_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of videos the author gained in the last week.
    """
    monthly_videos_change: Mapped[int] = mapped_column(Numeric)
    """
    Number of videos the author gained in the last month.
    """

    # Growth rates
    daily_followers_growth_rate: Mapped[float] = mapped_column(Numeric(10, 2))
    """
    Growth rate of followers in the last day.
    """
    weekly_followers_growth_rate: Mapped[float] = mapped_column(Numeric(10, 2))
    """
    Growth rate of followers in the last week.
    """
    monthly_followers_growth_rate: Mapped[float] = mapped_column(Numeric(10, 2))
    """
    Growth rate of followers in the last month.
    """

    def __repr__(self) -> str:
        """
        Return a string representation of the AuthorTrends object.

        This representation includes key attributes like author_id, collected_at,
        current_followers, daily_followers_change, weekly_followers_change, and
        monthly_followers_change, which are useful for debugging and logging.

        Returns:
            str: A string representation of the AuthorTrends object.
        """

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
        """
        Refresh the author_trends materialized view
        """
        await session.execute(text("REFRESH MATERIALIZED VIEW author_trends;"))
        await session.commit()
