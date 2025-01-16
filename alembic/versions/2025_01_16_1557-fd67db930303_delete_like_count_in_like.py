"""delete like_count in like

Revision ID: fd67db930303
Revises: ee1d076193b3
Create Date: 2025-01-16 15:57:03.977443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd67db930303'
down_revision: Union[str, None] = 'ee1d076193b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("like","like_count")


def downgrade() -> None:
    op.add_column("like",sa.Column("like_count",sa.Integer,server_default="0", nullable= False))
