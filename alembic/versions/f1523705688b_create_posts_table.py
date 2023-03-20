"""create posts table

Revision ID: f1523705688b
Revises: 
Create Date: 2023-03-17 13:27:16.024145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1523705688b'
down_revision = None
branch_labels = None
depends_on = None



def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
   op.drop_table('posts') 