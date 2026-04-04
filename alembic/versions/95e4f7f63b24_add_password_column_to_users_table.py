"""add password column to users table

Revision ID: 95e4f7f63b24
Revises: f8c13f352894
Create Date: 2026-04-03 17:53:23.648925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95e4f7f63b24'
down_revision: Union[str, Sequence[str], None] = 'f8c13f352894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE users
        ADD COLUMN password VARCHAR(200) NOT NULL""")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE users
        DROP COLUMN password""")
    pass
