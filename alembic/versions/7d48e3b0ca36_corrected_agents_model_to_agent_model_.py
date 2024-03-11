"""corrected agents_model to agent_model, removed agent_data_model

Revision ID: 7d48e3b0ca36
Revises: 5f97254b0b27
Create Date: 2024-03-11 12:50:00.655122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d48e3b0ca36'
down_revision: Union[str, None] = '5f97254b0b27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing table
    op.drop_table('agents')

    # Create a new table with the updated schema
    op.create_table('agents',
                    sa.Column('AgentID', sa.String(50), primary_key=True),
                    sa.Column('AgentName', sa.String(150), nullable=True),
                    sa.Column('GroupResourceID', sa.String(50), nullable=True),
                    sa.Column('GroupName', sa.String(150), nullable=True),
                    sa.Column('GroupParentID', sa.String(50), nullable=True),
                    sa.Column('Notes', sa.String(500), nullable=True),
                    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
                    sa.Column('LastModifiedOn', sa.DateTime(), nullable=True),
                    sa.Column('Enabled', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
                    sa.Column('RowUpdated', sa.DateTime(), nullable=True, server_default=sa.text('CURRENT_TIMESTAMP'))
                    )

def downgrade() -> None:
    def downgrade():
        # Drop the new schema table
        op.drop_table('agents')

        # Recreate the original table schema
        op.create_table('agents',
                        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
                        sa.Column('resourceID', sa.VARCHAR(length=50), nullable=False),
                        sa.Column('last_connectedID', sa.VARCHAR(length=50), nullable=False),
                        sa.Column('last_connected_machinename', sa.VARCHAR(length=50), nullable=False),
                        sa.Column('last_connect_datetime', sa.DateTime(), nullable=True),
                        sa.PrimaryKeyConstraint('id')
                        )
