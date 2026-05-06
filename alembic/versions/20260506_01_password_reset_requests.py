"""add password reset requests

Revision ID: 20260506_01
Revises: 20260430_01
Create Date: 2026-05-06 10:30:00
"""

import sqlalchemy as sa
from alembic import op


revision = "20260506_01"
down_revision = "20260430_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "password_reset_requests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("token", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("token"),
    )
    op.create_index("ix_password_reset_requests_company_id", "password_reset_requests", ["company_id"])
    op.create_index("ix_password_reset_requests_user_id", "password_reset_requests", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_password_reset_requests_user_id", table_name="password_reset_requests")
    op.drop_index("ix_password_reset_requests_company_id", table_name="password_reset_requests")
    op.drop_table("password_reset_requests")
