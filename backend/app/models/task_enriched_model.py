
"""
Enriched Task Data Model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base_model import Base  # pylint: disable=relative-beyond-top-level


class EnrichedTask(Base):  # pylint: disable=too-few-public-methods
    """
    This is the EnrichedTask class involving different details about a task enriched with metadata.
    from agent and trigger
    """
    __tablename__ = 'tasks'

    ID = Column(String(38), primary_key=True)
    WorkflowID = Column(String(38), nullable=True)
    ResourceName = Column(String(255), nullable=True)
    ConstructTypeName = Column(String(20), nullable=True)
    TaskAgentID = Column(String(38), nullable=True)
    Enabled = Column(Boolean, nullable=True)
    ItemType = Column(Integer, nullable=True)
    ConstructID = Column(String(38), nullable=True)
    ConstructType = Column(Integer, nullable=True)
    Expression = Column(String(255), nullable=True)
    ResourceType = Column(Integer, nullable=True)
    CompletionState = Column(Integer, nullable=True)
    Notes = Column(String(255), nullable=True)
    CreatedBy = Column(String(38), nullable=True)
    CreatedOn = Column(DateTime, nullable=True)
    ModifiedOn = Column(DateTime, nullable=True)
    Version = Column(Integer, nullable=True)
    VersionDate = Column(DateTime, nullable=True)
    Empty = Column(Boolean, nullable=True)
    Removed = Column(Boolean, nullable=True)
    ResultCode = Column(Integer, nullable=True)
    ResultText = Column(String(500), nullable=True)
    StartedOn = Column(DateTime, nullable=True)
    EndedOn = Column(DateTime, nullable=True)
    LockedBy = Column(String(38), nullable=True)
    SuccessCount = Column(Integer, nullable=True)
    FailureCount = Column(Integer, nullable=True)
    RowLastUpdated = Column(DateTime, nullable=True)
    AgentID = Column(String(38), nullable=True)
    AgentName = Column(String(255), nullable=True)
    AgentGroupResourceID = Column(String(38), nullable=True)
    AgentGroupName = Column(String(255), nullable=True)
    AgentGroupParentID = Column(String(38), nullable=True)
    AgentNotes = Column(String(255), nullable=True)
    AgentCreatedOn = Column(DateTime, nullable=True)
    AgentLastModifiedOn = Column(DateTime, nullable=True)
    AgentEnabled = Column(Boolean, nullable=True)
    AgentRowUpdated = Column(DateTime, nullable=True)
    TriggerID = Column(String(38), nullable=True)
    TriggerName = Column(String(255), nullable=True)
    TriggerType = Column(Integer, nullable=True)
    TriggerSource = Column(String(500), nullable=True)
    TriggerScheduleType = Column(Integer, nullable=True)
    TriggerLastLaunchDate = Column(DateTime, nullable=True)
    TriggerNextLaunchDate = Column(DateTime, nullable=True)
    TriggerFrequency = Column(Integer, nullable=True)
    TriggerRowUpdatedOn = Column(DateTime, nullable=True)
