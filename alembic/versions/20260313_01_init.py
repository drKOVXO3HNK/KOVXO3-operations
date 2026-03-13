"""init schema

Revision ID: 20260313_01
Revises: 
Create Date: 2026-03-13
"""
from alembic import op
import sqlalchemy as sa

revision = "20260313_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("fielditem",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("group_name", sa.String(), nullable=True),
        sa.Column("area_ha", sa.Float(), nullable=False, server_default="0")
    )
    op.create_table("cropitem",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False)
    )
    op.create_table("useritem",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("api_token", sa.String(), nullable=False)
    )
    op.create_table("auditlogitem",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("payload", sa.String(), nullable=True)
    )
    op.create_table("operationitem",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column("operation_type", sa.String(), nullable=False),
        sa.Column("field_id", sa.Integer(), nullable=False),
        sa.Column("crop_id", sa.Integer(), nullable=True),
        sa.Column("planned_area_ha", sa.Float(), nullable=False, server_default="0"),
        sa.Column("completed_area_ha", sa.Float(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(), nullable=False, server_default="planned"),
        sa.Column("planned_date", sa.Date(), nullable=True),
        sa.Column("completed_date", sa.Date(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_table("operationitem")
    op.drop_table("auditlogitem")
    op.drop_table("useritem")
    op.drop_table("cropitem")
    op.drop_table("fielditem")
