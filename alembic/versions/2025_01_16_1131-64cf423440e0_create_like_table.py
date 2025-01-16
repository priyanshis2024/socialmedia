"""Create like table

Revision ID: 64cf423440e0
Revises: 48ca8a7ad5eb
Create Date: 2025-01-16 11:31:48.328199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid 

# revision identifiers, used by Alembic.
revision: str = '64cf423440e0'
down_revision: Union[str, None] = '48ca8a7ad5eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'like',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('post_id', UUID(as_uuid=True), sa.ForeignKey('post.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('like_count', sa.Integer, server_default='1', nullable=False),  # Use server_default for default value
        sa.Column('is_liked', sa.Boolean, server_default='TRUE', nullable=False),  # Use server_default for boolean
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
    )

def downgrade() -> None:
    op.drop_table('like')