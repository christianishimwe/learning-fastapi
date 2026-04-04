"""create user_id column in posts and references id in user

Revision ID: b520c561eb66
Revises: 95e4f7f63b24
Create Date: 2026-04-03 20:48:36.488233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b520c561eb66'
down_revision: Union[str, Sequence[str], None] = '95e4f7f63b24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE posts
        ADD COLUMN user_id INTEGER NOT NULL REFERENCES users(id)
               """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE posts
        DROP COLUMN user_id""")
    pass
