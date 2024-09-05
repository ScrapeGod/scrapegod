"""create user table

Revision ID: 3bd8d5c87e98
Revises: 
Create Date: 2024-09-02 10:53:01.174425

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from lib.util_datetime import tzware_datetime


# revision identifiers, used by Alembic.
revision: str = "3bd8d5c87e98"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("username", sa.String(length=128), nullable=True),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
            server_default="",
            unique=True,
        ),
        sa.Column("password", sa.String(length=128), nullable=False, server_default=""),
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
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=False)
    # ### end Alembic commands ###

    # Create the 'api_key' table
    op.create_table(
        "api_key",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False),
        sa.Column("key", sa.String(length=128), nullable=False),
        sa.Column("revoked", sa.Boolean(), default=False),
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
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_username"), table_name="user")

    op.drop_table("api_key")
    op.drop_table("user")
    # ### end Alembic commands ###
