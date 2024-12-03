"""challenge_stats_materialized_view

Revision ID: e09dfb2b3d86
Revises: 36d31a642534
Create Date: 2024-12-02 20:38:07.787520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e09dfb2b3d86'
down_revision: Union[str, None] = '36d31a642534'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create materialized view
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS challenge_trends AS
        WITH latest_trends AS (
            SELECT 
                post_id,
                daily_growth_rate,
                weekly_growth_rate,
                monthly_growth_rate,
                collected_at,
                ROW_NUMBER() OVER (
                    PARTITION BY post_id 
                    ORDER BY collected_at DESC
                ) as rn
            FROM post_trends
        ),
        active_hashtag_challenges AS (
            -- Get challenges related to active hashtags
            SELECT 
                ah.id as hashtag_id,
                ah.title as hashtag_title,
                c.id as challenge_id,
                c.title as challenge_title
            FROM active_hashtags ah
            JOIN challenges c ON lower(c.title) LIKE '%' || lower(replace(ah.title, '#', '')) || '%'
            WHERE ah.active = true
        )
        SELECT 
            ahc.hashtag_id as challenge_id,
            ahc.hashtag_title as challenge_title,  -- Fixed typo in 'challenge_title'
            ROUND(AVG(t.daily_growth_rate)*100, 1) as daily_growth,
            ROUND(AVG(t.weekly_growth_rate)*100, 1) as weekly_growth,
            ROUND(AVG(t.monthly_growth_rate)*100, 1) as monthly_growth
        FROM active_hashtag_challenges ahc
        JOIN posts_challenges pc ON ahc.challenge_id = pc.challenge_id
        JOIN latest_trends t ON pc.post_id = t.post_id
        WHERE t.rn = 1
        GROUP BY ahc.hashtag_id, ahc.hashtag_title
    """)
    # Create indexes for the view columns
    op.execute("CREATE INDEX IF NOT EXISTS idx_challenge_trends_id ON challenge_trends(challenge_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_challenge_trends_title ON challenge_trends(challenge_title)")

def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS challenge_trends CASCADE")