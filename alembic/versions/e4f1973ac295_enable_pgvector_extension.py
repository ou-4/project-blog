"""Enable pgvector extension

Revision ID: e4f1973ac295
Revises: 09283e905bd8
Create Date: 2026-10-13 01:10:39.644851

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e4f1973ac295"
down_revision: str | Sequence[str] | None = "09283e905bd8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
