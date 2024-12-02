"""Add cognito_id column to users table

Revision ID: 7096a073f6b3
Revises: 4fe3eeed9a9d
Create Date: 2024-12-02 12:47:02.375881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7096a073f6b3'
down_revision = '4fe3eeed9a9d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("cognito_id", sa.String(length=36), nullable=True))


def downgrade():
    op.drop_column("users", "cognito_id")
