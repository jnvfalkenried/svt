"""authors materialized view

Revision ID: b7741cb1161c
Revises: e09dfb2b3d86
Create Date: 2024-12-17 09:07:16.518500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7741cb1161c'
down_revision: Union[str, None] = 'e09dfb2b3d86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create materialized view
    op.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS author_trends AS
        WITH time_period_changes AS (
            SELECT 
                id as author_id,
                collected_at,
                follower_count as current_followers,
                heart_count as current_hearts,
                digg_count as current_diggs,
                video_count as current_videos,
                
                -- Followers changes over time
                LAG(follower_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW
                ) as day_ago_followers,
                LAG(follower_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
                ) as week_ago_followers,
                LAG(follower_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '30 days' PRECEDING AND CURRENT ROW
                ) as month_ago_followers,
                
                -- Hearts changes over time
                LAG(heart_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW
                ) as day_ago_hearts,
                LAG(heart_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
                ) as week_ago_hearts,
                LAG(heart_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '30 days' PRECEDING AND CURRENT ROW
                ) as month_ago_hearts,
                
                -- Diggs changes over time
                LAG(digg_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW
                ) as day_ago_diggs,
                LAG(digg_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
                ) as week_ago_diggs,
                LAG(digg_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '30 days' PRECEDING AND CURRENT ROW
                ) as month_ago_diggs,
                
                -- Videos changes over time
                LAG(video_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW
                ) as day_ago_videos,
                LAG(video_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW
                ) as week_ago_videos,
                LAG(video_count) OVER (
                    PARTITION BY id 
                    ORDER BY collected_at
                    RANGE BETWEEN INTERVAL '30 days' PRECEDING AND CURRENT ROW
                ) as month_ago_videos
            FROM authors_reporting
            WHERE follower_count IS NOT NULL
        )
        SELECT 
            author_id,
            collected_at,
            current_followers,
            current_hearts,
            current_diggs,
            current_videos,
            
            -- Followers changes
            COALESCE(current_followers - day_ago_followers, 0) as daily_followers_change,
            COALESCE(current_followers - week_ago_followers, 0) as weekly_followers_change,
            COALESCE(current_followers - month_ago_followers, 0) as monthly_followers_change,
            
            -- Hearts changes
            COALESCE(current_hearts - day_ago_hearts, 0) as daily_hearts_change,
            COALESCE(current_hearts - week_ago_hearts, 0) as weekly_hearts_change,
            COALESCE(current_hearts - month_ago_hearts, 0) as monthly_hearts_change,
            
            -- Diggs changes
            COALESCE(current_diggs - day_ago_diggs, 0) as daily_diggs_change,
            COALESCE(current_diggs - week_ago_diggs, 0) as weekly_diggs_change,
            COALESCE(current_diggs - month_ago_diggs, 0) as monthly_diggs_change,
            
            -- Videos changes
            COALESCE(current_videos - day_ago_videos, 0) as daily_videos_change,
            COALESCE(current_videos - week_ago_videos, 0) as weekly_videos_change,
            COALESCE(current_videos - month_ago_videos, 0) as monthly_videos_change,
            
            -- Growth rates
            CASE 
                WHEN day_ago_followers > 0 THEN 
                    ((current_followers - day_ago_followers)::float / day_ago_followers * 100)::numeric(10,2)
                ELSE 0 
            END as daily_followers_growth_rate,
            CASE 
                WHEN week_ago_followers > 0 THEN 
                    ((current_followers - week_ago_followers)::float / week_ago_followers * 100)::numeric(10,2)
                ELSE 0 
            END as weekly_followers_growth_rate,
            CASE 
                WHEN month_ago_followers > 0 THEN 
                    ((current_followers - month_ago_followers)::float / month_ago_followers * 100)::numeric(10,2)
                ELSE 0 
            END as monthly_followers_growth_rate
        FROM time_period_changes
        """
    )
    
    # Create indexes for better query performance
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_author_trends_author_id 
        ON author_trends(author_id)
        """
    )
    
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_author_trends_collected_at 
        ON author_trends(collected_at)
        """
    )
    
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_author_trends_followers_changes 
        ON author_trends(daily_followers_change, weekly_followers_change, monthly_followers_change)
        """
    )
    
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_author_trends_growth_rates 
        ON author_trends(daily_followers_growth_rate, weekly_followers_growth_rate, monthly_followers_growth_rate)
        """
    )


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS author_trends CASCADE")