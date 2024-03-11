"""added task model

Revision ID: c6b80feaf300
Revises: 2f64c72aae10
Create Date: 2024-03-11 18:37:00.089801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6b80feaf300'
down_revision: Union[str, None] = '2f64c72aae10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
