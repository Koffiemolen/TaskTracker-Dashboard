"""corrected agent_model, removed primary key id column

Revision ID: 2f64c72aae10
Revises: 7d48e3b0ca36
Create Date: 2024-03-11 12:52:35.994828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f64c72aae10'
down_revision: Union[str, None] = '7d48e3b0ca36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
