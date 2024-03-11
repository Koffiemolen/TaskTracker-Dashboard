"""Add custom SQL elements, eg: view for triggers, functions for extracting data

Revision ID: 5f97254b0b27
Revises: de4628a6bc9e
Create Date: 2024-03-11 12:28:19.692040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f97254b0b27'
down_revision: Union[str, None] = 'de4628a6bc9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
