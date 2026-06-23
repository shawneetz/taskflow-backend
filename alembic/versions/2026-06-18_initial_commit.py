"""initial commit

Revision ID: a1ee73811560
Revises: 60c53a61a707
Create Date: 2026-06-18 00:25:48.244664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1ee73811560'
down_revision: Union[str, Sequence[str], None] = '60c53a61a707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
