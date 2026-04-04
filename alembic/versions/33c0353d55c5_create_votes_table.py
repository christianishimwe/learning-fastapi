"""create votes table

Revision ID: 33c0353d55c5
Revises: b520c561eb66
Create Date: 2026-04-03 20:59:38.156500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33c0353d55c5'
down_revision: Union[str, Sequence[str], None] = 'b520c561eb66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE votes (
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
            PRIMARY KEY (user_id, post_id)
        )""")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE votes""")
    pass
