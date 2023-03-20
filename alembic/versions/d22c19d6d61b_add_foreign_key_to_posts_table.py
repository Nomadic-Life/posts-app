"""add foreign-key to posts table

Revision ID: d22c19d6d61b
Revises: 7945390c6421
Create Date: 2023-03-17 17:02:01.874055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd22c19d6d61b'
down_revision = '7945390c6421'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts" )
    op.drop_column('posts', 'owner_id')
