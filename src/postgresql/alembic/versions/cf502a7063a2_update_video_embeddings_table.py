"""update_video_embeddings_table

Revision ID: cf502a7063a2
Revises: dfd5d2f8ed32
Create Date: 2024-11-06 21:23:27.917294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector



# revision identifiers, used by Alembic.
revision: str = 'cf502a7063a2'
down_revision: Union[str, None] = 'dfd5d2f8ed32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Rename the old table to backup
    op.rename_table('video_embeddings', 'video_embeddings_backup')
    
    # Create new table with desired structure
    op.create_table(
        'video_embeddings',
        sa.Column('post_id', sa.String(), nullable=False),
        sa.Column('element_id', sa.Integer(), nullable=False),
        sa.Column('embedding', Vector(1408)),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('post_id', 'element_id')
    )

    # Migrate data from old table to new table
    op.execute("""
        INSERT INTO video_embeddings (post_id, element_id, embedding)
        SELECT 
            id,
            ROW_NUMBER() OVER (ORDER BY inserted_at) as element_id,
            video_embedding
        FROM video_embeddings_backup;
    """)

    # Create index for better query performance
    op.create_index(
        'idx_video_embeddings_post_id',
        'video_embeddings',
        ['post_id']
    )

    # If everything went well, drop the backup table
    op.drop_table('video_embeddings_backup')

def downgrade():
    # Create the original table structure
    op.create_table(
        'video_embeddings_backup',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('video_embedding', Vector(1408)),
        sa.Column('description_embedding', Vector(1408)),
        sa.Column('description', sa.Text()),
        sa.Column('inserted_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['id'], ['posts.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data back
    op.execute("""
        INSERT INTO video_embeddings_backup (id, video_embedding)
        SELECT post_id, embedding
        FROM video_embeddings;
    """)

    # Drop new table
    op.drop_table('video_embeddings')

    # Rename backup table to original name
    op.rename_table('video_embeddings_backup', 'video_embeddings')