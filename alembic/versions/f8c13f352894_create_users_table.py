"""create users table

Revision ID: f8c13f352894
Revises: 844406263f5c
Create Date: 2026-04-03 17:46:59.345883

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8c13f352894'
down_revision: Union[str, Sequence[str], None] = '844406263f5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(200) UNIQUE NOT NULL)
            """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""DROP TABLE users""")
    pass
