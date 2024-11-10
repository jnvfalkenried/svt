"""empty message

Revision ID: d60ff69d550b
Revises: 7c71c7f370f7, a350d835dadf
Create Date: 2024-11-10 20:51:33.923666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd60ff69d550b'
down_revision: Union[str, None] = ('7c71c7f370f7', 'a350d835dadf')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
