"""create meetings table

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-21

"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "meetings",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("transcript", sa.Text(), nullable=False),
        sa.Column(
            "department_id", sa.Uuid(), sa.ForeignKey("departments.id"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_table("meetings")
