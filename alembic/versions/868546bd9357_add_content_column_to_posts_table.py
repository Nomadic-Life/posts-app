"""add content column to posts table

Revision ID: 868546bd9357
Revises: f1523705688b
Create Date: 2023-03-17 16:43:23.209103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '868546bd9357'
down_revision = 'f1523705688b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
