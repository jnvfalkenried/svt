"""create_post_trends_view

Revision ID: f7382c647ead
Revises: 4fdfcea4fa83
Create Date: 2024-11-28 09:18:56.001198

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f7382c647ead"
down_revision: Union[str, None] = "4fdfcea4fa83"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create materialized view
    op.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS post_trends AS
        WITH time_period_changes AS (
            SELECT 
                id as post_id,
                collected_at,
                CAST(NULLIF(play_count, '') AS NUMERIC) as current_views,
                LAG(CAST(NULLIF(play_count, '') AS NUMERIC)) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW
                ) as day_ago_views,
                LAG(CAST(NULLIF(play_count, '') AS NUMERIC)) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
                ) as week_ago_views,
                LAG(CAST(NULLIF(play_count, '') AS NUMERIC)) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '30 days' PRECEDING AND CURRENT ROW
                ) as month_ago_views
            FROM posts_reporting
            WHERE play_count IS NOT NULL AND play_count != ''
        )
        SELECT 
            post_id,
            collected_at,
            current_views,
            COALESCE(current_views - day_ago_views, 0) as daily_change,
            COALESCE(current_views - week_ago_views, 0) as weekly_change,
            COALESCE(current_views - month_ago_views, 0) as monthly_change,
            CASE 
                WHEN day_ago_views > 0 THEN 
                    ((current_views - day_ago_views) / day_ago_views * 100)::numeric(10,2)
                ELSE 0 
            END as daily_growth_rate,
            CASE 
                WHEN week_ago_views > 0 THEN 
                    ((current_views - week_ago_views) / week_ago_views * 100)::numeric(10,2)
                ELSE 0 
            END as weekly_growth_rate,
            CASE 
                WHEN month_ago_views > 0 THEN 
                    ((current_views - month_ago_views) / month_ago_views * 100)::numeric(10,2)
                ELSE 0 
            END as monthly_growth_rate
        FROM time_period_changes
    """
    )

    # Create indexes separately
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_post_trends_post_id 
        ON post_trends(post_id)
    """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_post_trends_collected_at 
        ON post_trends(collected_at)
    """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_post_trends_daily_change 
        ON post_trends(daily_change)
    """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_post_trends_weekly_change 
        ON post_trends(weekly_change)
    """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_post_trends_monthly_change 
        ON post_trends(monthly_change)
    """
    )


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS post_trends CASCADE")
