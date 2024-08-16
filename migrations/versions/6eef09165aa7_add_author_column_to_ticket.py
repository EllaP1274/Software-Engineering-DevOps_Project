"""Add author column to Ticket

Revision ID: 6eef09165aa7
Revises: 5460838c7a92
Create Date: 2024-08-16 14:27:33.615602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eef09165aa7'
down_revision = '5460838c7a92'
branch_labels = None
depends_on = None

def upgrade():
    # Add the 'author' column with a default value (if needed)
    op.add_column('ticket', sa.Column('author', sa.String(length=150), nullable=True))

def downgrade():
    # Remove the 'author' column if downgrading
    op.drop_column('ticket', 'author')

