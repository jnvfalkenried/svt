"""Add url columns to posts, posts_reporting

Revision ID: 36d31a642534
Revises: 16b35331d1e2
Create Date: 2024-12-02 07:01:53.051821

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "36d31a642534"
down_revision: Union[str, None] = "16b35331d1e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("posts", sa.Column("url", sa.String(), nullable=True))
    op.add_column("posts_reporting", sa.Column("url", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts_reporting", "url")
    op.drop_column("posts", "url")
    # ### end Alembic commands ###
