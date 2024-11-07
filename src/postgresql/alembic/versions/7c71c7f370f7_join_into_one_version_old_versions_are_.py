"""join into one version, old versions are affecting

Revision ID: 7c71c7f370f7
Revises: d0b6aa31351d
Create Date: 2024-11-06 22:47:54.802421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '7c71c7f370f7'
down_revision: Union[str, None] = 'd0b6aa31351d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'video_embeddings',
        sa.Column('post_id', sa.String(), nullable=False),
        sa.Column('element_id', sa.Integer(), nullable=False),
        sa.Column('embedding', Vector(1408)),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('post_id', 'element_id')
    )
    op.create_index(
        'idx_video_embeddings_post_id',
        'video_embeddings',
        ['post_id']
    )

def downgrade():
    op.drop_table('video_embeddings')
