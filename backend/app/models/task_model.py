
"""
Task Data Model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .base_model import Base  # pylint: disable=relative-beyond-top-level


class Task(Base):  # pylint: disable=too-few-public-methods
    """
    This is the Task class involving details about a task.
    """
    __tablename__ = 'tasksinfo'

    ID = Column(String(38), primary_key=True)
    WorkflowID = Column(String(38), nullable=True)
    ResourceName = Column(String(255), nullable=True)
    ConstructTypeName = Column(String(20), nullable=True)
    AgentID = Column(String(38), nullable=True)
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
    Enabled = Column(Boolean, nullable=True)
    Removed = Column(Boolean, nullable=True)
    ResultCode = Column(Integer, nullable=True)
    ResultText = Column(String(500), nullable=True)
    StartedOn = Column(DateTime, nullable=True)
    EndedOn = Column(DateTime, nullable=True)
    LockedBy = Column(String(38), nullable=True)
    SuccessCount = Column(Integer, nullable=True)
    FailureCount = Column(Integer, nullable=True)
    RowLastUpdated = Column(DateTime, nullable=True)
