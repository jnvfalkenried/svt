"""Active hashtags table

Revision ID: c79ecf4c5a69
Revises: d60ff69d550b
Create Date: 2024-11-12 11:02:22.848590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c79ecf4c5a69'
down_revision: Union[str, None] = 'd60ff69d550b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active_hashtags',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('inserted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'active')
    )
    op.drop_index('idx_video_embeddings_post_id', table_name='video_embeddings')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_video_embeddings_post_id', 'video_embeddings', ['post_id'], unique=False)
    op.drop_table('active_hashtags')
    # ### end Alembic commands ###
