"""add diary module tables

Revision ID: 20260506_02
Revises: 20260506_01
Create Date: 2026-05-06 12:00:00
"""

import sqlalchemy as sa
from alembic import op


revision = "20260506_02"
down_revision = "20260506_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "diary_team_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("construction_diaries.id"), nullable=False),
        sa.Column("total_workers", sa.Integer(), nullable=False),
        sa.Column("total_hours", sa.Integer(), nullable=False),
        sa.Column("highlight_role", sa.String(length=120), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_diary_team_entries_company_id", "diary_team_entries", ["company_id"])
    op.create_index("ix_diary_team_entries_diary_id", "diary_team_entries", ["diary_id"])

    op.create_table(
        "diary_activity_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("construction_diaries.id"), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_diary_activity_entries_company_id", "diary_activity_entries", ["company_id"])
    op.create_index("ix_diary_activity_entries_diary_id", "diary_activity_entries", ["diary_id"])

    op.create_table(
        "diary_material_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("construction_diaries.id"), nullable=False),
        sa.Column("material_name", sa.String(length=160), nullable=False),
        sa.Column("quantity_label", sa.String(length=80), nullable=True),
        sa.Column("movement_type", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_diary_material_entries_company_id", "diary_material_entries", ["company_id"])
    op.create_index("ix_diary_material_entries_diary_id", "diary_material_entries", ["diary_id"])

    op.create_table(
        "diary_equipment_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("construction_diaries.id"), nullable=False),
        sa.Column("equipment_name", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("usage_hours", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_diary_equipment_entries_company_id", "diary_equipment_entries", ["company_id"])
    op.create_index("ix_diary_equipment_entries_diary_id", "diary_equipment_entries", ["diary_id"])

    op.create_table(
        "diary_occurrence_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("construction_diaries.id"), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("responsible", sa.String(length=120), nullable=True),
        sa.Column("action_taken", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_diary_occurrence_entries_company_id", "diary_occurrence_entries", ["company_id"])
    op.create_index("ix_diary_occurrence_entries_diary_id", "diary_occurrence_entries", ["diary_id"])

    op.create_table(
        "diary_photo_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("construction_diaries.id"), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=True),
        sa.Column("location", sa.String(length=160), nullable=True),
        sa.Column("file_url", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_diary_photo_entries_company_id", "diary_photo_entries", ["company_id"])
    op.create_index("ix_diary_photo_entries_diary_id", "diary_photo_entries", ["diary_id"])


def downgrade() -> None:
    op.drop_index("ix_diary_photo_entries_diary_id", table_name="diary_photo_entries")
    op.drop_index("ix_diary_photo_entries_company_id", table_name="diary_photo_entries")
    op.drop_table("diary_photo_entries")

    op.drop_index("ix_diary_occurrence_entries_diary_id", table_name="diary_occurrence_entries")
    op.drop_index("ix_diary_occurrence_entries_company_id", table_name="diary_occurrence_entries")
    op.drop_table("diary_occurrence_entries")

    op.drop_index("ix_diary_equipment_entries_diary_id", table_name="diary_equipment_entries")
    op.drop_index("ix_diary_equipment_entries_company_id", table_name="diary_equipment_entries")
    op.drop_table("diary_equipment_entries")

    op.drop_index("ix_diary_material_entries_diary_id", table_name="diary_material_entries")
    op.drop_index("ix_diary_material_entries_company_id", table_name="diary_material_entries")
    op.drop_table("diary_material_entries")

    op.drop_index("ix_diary_activity_entries_diary_id", table_name="diary_activity_entries")
    op.drop_index("ix_diary_activity_entries_company_id", table_name="diary_activity_entries")
    op.drop_table("diary_activity_entries")

    op.drop_index("ix_diary_team_entries_diary_id", table_name="diary_team_entries")
    op.drop_index("ix_diary_team_entries_company_id", table_name="diary_team_entries")
    op.drop_table("diary_team_entries")
