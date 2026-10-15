"""Add GIN index for article search

Revision ID: 09283e905bd8
Revises: d495826ea3b8
Create Date: 2026-09-21 13:40:03.634774

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "09283e905bd8"
down_revision: str | Sequence[str] | None = "d495826ea3b8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX idx_articles_search ON articles
        USING GIN (to_tsvector('russian', title || ' ' || content))
    """)


def downgrade() -> None:
    op.execute("DROP INDEX idx_articles_search")
