"""add_vector_extension

Revision ID: d0b6aa31351d
Revises: 4cd2361f4aeb
Create Date: 2024-11-06 22:10:08.455270

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d0b6aa31351d"
down_revision: Union[str, None] = "4cd2361f4aeb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS vector")
