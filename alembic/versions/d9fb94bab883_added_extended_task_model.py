"""added extended task model

Revision ID: d9fb94bab883
Revises: c6b80feaf300
Create Date: 2024-03-17 16:17:00.784378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9fb94bab883'
down_revision: Union[str, None] = 'c6b80feaf300'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
