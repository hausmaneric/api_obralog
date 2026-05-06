"""initial schema

Revision ID: 20260430_01
Revises:
Create Date: 2026-04-30 15:20:00
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = "20260430_01"
down_revision = None
branch_labels = None
depends_on = None


user_role = postgresql.ENUM("owner", "engineer", "foreman", "viewer", name="userrole", create_type=False)
work_status = postgresql.ENUM("planned", "in_progress", "paused", "finished", "cancelled", name="workstatus", create_type=False)
diary_status = postgresql.ENUM("draft", "submitted", "approved", "rejected", "locked", name="dairystatus", create_type=False)

user_role_create = postgresql.ENUM("owner", "engineer", "foreman", "viewer", name="userrole")
work_status_create = postgresql.ENUM("planned", "in_progress", "paused", "finished", "cancelled", name="workstatus")
diary_status_create = postgresql.ENUM("draft", "submitted", "approved", "rejected", "locked", name="dairystatus")


def upgrade() -> None:
    bind = op.get_bind()
    user_role_create.create(bind, checkfirst=True)
    work_status_create.create(bind, checkfirst=True)
    diary_status_create.create(bind, checkfirst=True)

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("cnpj", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=120), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_company_id", "users", ["company_id"])

    op.create_table(
        "works",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("client_name", sa.String(length=120), nullable=True),
        sa.Column("city", sa.String(length=80), nullable=True),
        sa.Column("state", sa.String(length=2), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("expected_end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", work_status, nullable=False),
        sa.Column("progress_percentage", sa.Float(), nullable=False),
    )
    op.create_index("ix_works_company_id", "works", ["company_id"])

    op.create_table(
        "construction_diaries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("work_id", sa.Integer(), sa.ForeignKey("works.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("number", sa.String(length=20), nullable=False),
        sa.Column("responsible_name", sa.String(length=120), nullable=False),
        sa.Column("weather_morning", sa.String(length=80), nullable=True),
        sa.Column("weather_afternoon", sa.String(length=80), nullable=True),
        sa.Column("weather_night", sa.String(length=80), nullable=True),
        sa.Column("rain", sa.String(length=30), nullable=True),
        sa.Column("rain_impact", sa.Text(), nullable=True),
        sa.Column("general_notes", sa.Text(), nullable=True),
        sa.Column("status", diary_status, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("work_id", "date", name="uq_work_date"),
    )
    op.create_index("ix_construction_diaries_company_id", "construction_diaries", ["company_id"])
    op.create_index("ix_construction_diaries_work_id", "construction_diaries", ["work_id"])


def downgrade() -> None:
    op.drop_index("ix_construction_diaries_work_id", table_name="construction_diaries")
    op.drop_index("ix_construction_diaries_company_id", table_name="construction_diaries")
    op.drop_table("construction_diaries")

    op.drop_index("ix_works_company_id", table_name="works")
    op.drop_table("works")

    op.drop_index("ix_users_company_id", table_name="users")
    op.drop_table("users")

    op.drop_table("companies")

    bind = op.get_bind()
    diary_status_create.drop(bind, checkfirst=True)
    work_status_create.drop(bind, checkfirst=True)
    user_role_create.drop(bind, checkfirst=True)
