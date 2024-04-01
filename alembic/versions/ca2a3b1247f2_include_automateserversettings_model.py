"""Include AutomateServerSettings model

Revision ID: ca2a3b1247f2
Revises: 655a843dc911
Create Date: 2024-03-31 11:13:44.108447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2a3b1247f2'
down_revision: Union[str, None] = '655a843dc911'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('automateserversettings',
    sa.Column('ID', sa.String(length=38), nullable=False),
    sa.Column('UseIPFilters', sa.Boolean(), nullable=True),
    sa.Column('BlockListType', sa.Integer(), nullable=True),
    sa.Column('BlockedIPList', sa.String(length=255), nullable=True),
    sa.Column('DefaultIPFiltersAllow', sa.Boolean(), nullable=True),
    sa.Column('UseSSL', sa.Boolean(), nullable=True),
    sa.Column('CertStoreLocation', sa.Integer(), nullable=True),
    sa.Column('CertStoreName', sa.Integer(), nullable=True),
    sa.Column('CertSearchType', sa.Integer(), nullable=True),
    sa.Column('CertSearchValue', sa.String(length=512), nullable=True),
    sa.Column('SMTPServer', sa.String(length=256), nullable=True),
    sa.Column('SMTPPort', sa.Integer(), nullable=True),
    sa.Column('SMTPUser', sa.String(length=512), nullable=True),
    sa.Column('SMTPPassword', sa.String(length=512), nullable=True),
    sa.Column('ErrorNotifyEmailToAddress', sa.String(length=256), nullable=True),
    sa.Column('ErrorNotifyEmailFromAddress', sa.String(length=256), nullable=True),
    sa.Column('ErrorRunTaskName', sa.String(length=128), nullable=True),
    sa.Column('UseLowestCompletionState', sa.Boolean(), nullable=True),
    sa.Column('LowestCompletionState', sa.Integer(), nullable=True),
    sa.Column('TrimTimeFrame', sa.Integer(), nullable=True),
    sa.Column('TrimCount', sa.Integer(), nullable=True),
    sa.Column('InstancesTrimTimeFrame', sa.Integer(), nullable=True),
    sa.Column('InstancesTrimCount', sa.Integer(), nullable=True),
    sa.Column('TaskStepsTrimTimeFrame', sa.Integer(), nullable=True),
    sa.Column('TaskStepsTrimCount', sa.Integer(), nullable=True),
    sa.Column('MaxRunningWorkflows', sa.Integer(), nullable=True),
    sa.Column('WorkflowDelayAfterStartup', sa.Integer(), nullable=True),
    sa.Column('DefaultStaging', sa.Integer(), nullable=True),
    sa.Column('Versioned', sa.Boolean(), nullable=True),
    sa.Column('VersionBehavior', sa.Integer(), nullable=True),
    sa.Column('VersionTrimValue', sa.Integer(), nullable=True),
    sa.Column('GlobalTriggering', sa.Boolean(), nullable=True),
    sa.Column('EnableLockout', sa.Boolean(), nullable=True),
    sa.Column('LockoutPeriod', sa.Integer(), nullable=True),
    sa.Column('AttemptPeriod', sa.Integer(), nullable=True),
    sa.Column('AttemptCount', sa.Integer(), nullable=True),
    sa.Column('EnableTimeout', sa.Boolean(), nullable=True),
    sa.Column('TimeoutPeriod', sa.Integer(), nullable=True),
    sa.Column('TimeoutUserIDs', sa.String(length=255), nullable=True),
    sa.Column('DisableConcurrentLogin', sa.Boolean(), nullable=True),
    sa.Column('EnableAPI', sa.Boolean(), nullable=True),
    sa.Column('EnableStepLogging', sa.Boolean(), nullable=True),
    sa.Column('AuditEventsTrimTimeFrame', sa.Integer(), nullable=True),
    sa.Column('AuditEventsTrimCount', sa.Integer(), nullable=True),
    sa.Column('PCMMinimumLength', sa.Integer(), nullable=True),
    sa.Column('PCMAllowLowercase', sa.Boolean(), nullable=True),
    sa.Column('PCMMinimumLowercase', sa.Integer(), nullable=True),
    sa.Column('PCMAllowUppercase', sa.Boolean(), nullable=True),
    sa.Column('PCMMinimumUppercase', sa.Integer(), nullable=True),
    sa.Column('PCMAllowNumbers', sa.Boolean(), nullable=True),
    sa.Column('PCMMinimumNumbers', sa.Integer(), nullable=True),
    sa.Column('PCMAllowSpecCharacters', sa.Boolean(), nullable=True),
    sa.Column('PCMMinimumSpecCharacters', sa.Integer(), nullable=True),
    sa.Column('PCMEnablePasswordExpiration', sa.Boolean(), nullable=True),
    sa.Column('PCMPasswordExpirationPeriod', sa.Integer(), nullable=True),
    sa.Column('PCMEnablePasswordHistory', sa.Boolean(), nullable=True),
    sa.Column('PCMEnforcePasswordHistory', sa.Integer(), nullable=True),
    sa.Column('EnableCustomActions', sa.Boolean(), nullable=True),
    sa.Column('RowLastUpdated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('tasksinfo',
    sa.Column('ID', sa.String(length=38), nullable=False),
    sa.Column('WorkflowID', sa.String(length=38), nullable=True),
    sa.Column('ResourceName', sa.String(length=255), nullable=True),
    sa.Column('ConstructTypeName', sa.String(length=20), nullable=True),
    sa.Column('AgentID', sa.String(length=38), nullable=True),
    sa.Column('ItemType', sa.Integer(), nullable=True),
    sa.Column('ConstructID', sa.String(length=38), nullable=True),
    sa.Column('ConstructType', sa.Integer(), nullable=True),
    sa.Column('Expression', sa.String(length=255), nullable=True),
    sa.Column('ResourceType', sa.Integer(), nullable=True),
    sa.Column('CompletionState', sa.Integer(), nullable=True),
    sa.Column('Notes', sa.String(length=255), nullable=True),
    sa.Column('CreatedBy', sa.String(length=38), nullable=True),
    sa.Column('CreatedOn', sa.DateTime(), nullable=True),
    sa.Column('ModifiedOn', sa.DateTime(), nullable=True),
    sa.Column('Version', sa.Integer(), nullable=True),
    sa.Column('VersionDate', sa.DateTime(), nullable=True),
    sa.Column('Empty', sa.Boolean(), nullable=True),
    sa.Column('Enabled', sa.Boolean(), nullable=True),
    sa.Column('Removed', sa.Boolean(), nullable=True),
    sa.Column('ResultCode', sa.Integer(), nullable=True),
    sa.Column('ResultText', sa.String(length=500), nullable=True),
    sa.Column('StartedOn', sa.DateTime(), nullable=True),
    sa.Column('EndedOn', sa.DateTime(), nullable=True),
    sa.Column('LockedBy', sa.String(length=38), nullable=True),
    sa.Column('SuccessCount', sa.Integer(), nullable=True),
    sa.Column('FailureCount', sa.Integer(), nullable=True),
    sa.Column('RowLastUpdated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('ID')
    )
    op.add_column('tasks', sa.Column('TaskAgentID', sa.String(length=38), nullable=True))
    op.add_column('tasks', sa.Column('AgentName', sa.String(length=255), nullable=True))
    op.add_column('tasks', sa.Column('AgentGroupResourceID', sa.String(length=38), nullable=True))
    op.add_column('tasks', sa.Column('AgentGroupName', sa.String(length=255), nullable=True))
    op.add_column('tasks', sa.Column('AgentGroupParentID', sa.String(length=38), nullable=True))
    op.add_column('tasks', sa.Column('AgentNotes', sa.String(length=255), nullable=True))
    op.add_column('tasks', sa.Column('AgentCreatedOn', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('AgentLastModifiedOn', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('AgentEnabled', sa.Boolean(), nullable=True))
    op.add_column('tasks', sa.Column('AgentRowUpdated', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('TriggerID', sa.String(length=38), nullable=True))
    op.add_column('tasks', sa.Column('TriggerName', sa.String(length=255), nullable=True))
    op.add_column('tasks', sa.Column('TriggerType', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('TriggerSource', sa.String(length=500), nullable=True))
    op.add_column('tasks', sa.Column('TriggerScheduleType', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('TriggerLastLaunchDate', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('TriggerNextLaunchDate', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('TriggerFrequency', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('TriggerRowUpdatedOn', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'TriggerRowUpdatedOn')
    op.drop_column('tasks', 'TriggerFrequency')
    op.drop_column('tasks', 'TriggerNextLaunchDate')
    op.drop_column('tasks', 'TriggerLastLaunchDate')
    op.drop_column('tasks', 'TriggerScheduleType')
    op.drop_column('tasks', 'TriggerSource')
    op.drop_column('tasks', 'TriggerType')
    op.drop_column('tasks', 'TriggerName')
    op.drop_column('tasks', 'TriggerID')
    op.drop_column('tasks', 'AgentRowUpdated')
    op.drop_column('tasks', 'AgentEnabled')
    op.drop_column('tasks', 'AgentLastModifiedOn')
    op.drop_column('tasks', 'AgentCreatedOn')
    op.drop_column('tasks', 'AgentNotes')
    op.drop_column('tasks', 'AgentGroupParentID')
    op.drop_column('tasks', 'AgentGroupName')
    op.drop_column('tasks', 'AgentGroupResourceID')
    op.drop_column('tasks', 'AgentName')
    op.drop_column('tasks', 'TaskAgentID')
    op.drop_table('tasksinfo')
    op.drop_table('automateserversettings')
    # ### end Alembic commands ###
