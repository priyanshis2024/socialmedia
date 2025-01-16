"""add likecount in post

Revision ID: ee1d076193b3
Revises: 64cf423440e0
Create Date: 2025-01-16 15:51:13.573344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee1d076193b3'
down_revision: Union[str, None] = '64cf423440e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("likecount",sa.Integer, server_default="0", nullable= False))


def downgrade() -> None:
    op.drop_column("post","likecount")
