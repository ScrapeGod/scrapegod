"""free proxy

Revision ID: 93df661bc27e
Revises: 3bd8d5c87e98
Create Date: 2024-09-09 15:28:23.911434

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from lib.util_datetime import tzware_datetime

# revision identifiers, used by Alembic.
revision: str = "93df661bc27e"
down_revision: Union[str, None] = "3bd8d5c87e98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum definitions
protocol_enum = sa.Enum("HTTP", "HTTPS", "SOCKS4", "SOCKS5", name="protocol_enum")
anonymity_enum = sa.Enum("ELITE", "ANONYMOUS", "TRANSPARENT", name="anonymity_enum")


def upgrade():

    # Create table
    op.create_table(
        "free_proxy",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ip_address", sa.String(length=100), nullable=False, unique=True),
        sa.Column("port", sa.String(length=10), nullable=False),
        sa.Column("protocol", protocol_enum, nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("anonymity", anonymity_enum, nullable=True),
        sa.Column("response_time", sa.Float(), nullable=True),
        sa.Column("last_checked", sa.DateTime(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
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
    )


def downgrade():
    # Drop table
    op.drop_table("free_proxy")
    # Drop enums
    # Drop enums
    op.execute("DROP TYPE protocol_enum")
    op.execute("DROP TYPE anonymity_enum")
