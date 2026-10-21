"""create hospitals and departments tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-21

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "hospitals",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
    )
    op.create_table(
        "departments",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "hospital_id", sa.Uuid(), sa.ForeignKey("hospitals.id"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("departments")
    op.drop_table("hospitals")
