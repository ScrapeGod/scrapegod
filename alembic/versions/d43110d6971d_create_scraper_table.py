"""create scraper table

Revision ID: d43110d6971d
Revises: 3bd8d5c87e98
Create Date: 2025-04-25 09:58:52.275125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from lib.util_datetime import tzware_datetime


# revision identifiers, used by Alembic.
revision: str = 'd43110d6971d'
down_revision: Union[str, None] = '3bd8d5c87e98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the scraper table
    op.create_table(
        'scraper',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('lambda_link', sa.String(length=256), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=True, server_default='active'),
        sa.Column(
            "created_on",
            sa.DateTime(timezone=True),
            nullable=False,
            default=tzware_datetime,
        ),
        sa.Column(
            "updated_on",
            sa.DateTime(timezone=True),
            nullable=False,
            default=tzware_datetime,
            onupdate=tzware_datetime,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    # Drop the scraper table
    op.drop_table('scraper')
