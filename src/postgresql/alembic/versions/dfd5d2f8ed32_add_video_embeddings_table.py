"""add_video_embeddings_table
Revision ID: dfd5d2f8ed32
Revises: 4cd2361f4aeb
Create Date: 2024-11-03 22:04:53.659657
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = 'dfd5d2f8ed32'
down_revision: Union[str, None] = '4cd2361f4aeb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create extension if not exists
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    
    # Create video_embeddings table
    op.create_table(
        'video_embeddings',
        sa.Column('id', sa.String(), primary_key=True),  # This will be your video_id
        sa.Column('video_embedding', Vector(1408)),  # Using pgvector's Vector type
        sa.Column('description_embedding', Vector(1408)),  # Using pgvector's Vector type
        sa.Column('description', sa.Text()),
        sa.Column('inserted_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        # Add foreign key to posts table
        sa.ForeignKeyConstraint(['id'], ['posts.id'], name='fk_video_embeddings_post_id')
    )
    
    # Create indexes for vector similarity search
    op.execute(
        'CREATE INDEX video_embedding_idx ON video_embeddings '
        'USING ivfflat (video_embedding vector_cosine_ops) WITH (lists = 100);'
    )
    op.execute(
        'CREATE INDEX description_embedding_idx ON video_embeddings '
        'USING ivfflat (description_embedding vector_cosine_ops) WITH (lists = 100);'
    )

def downgrade():
    # Drop indexes first
    op.execute('DROP INDEX IF EXISTS video_embedding_idx;')
    op.execute('DROP INDEX IF EXISTS description_embedding_idx;')
    
    # Drop the table
    op.drop_table('video_embeddings')