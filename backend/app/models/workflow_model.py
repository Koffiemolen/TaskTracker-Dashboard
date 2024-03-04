"""
Workflow Model
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from .base_model import Base  # pylint: disable=relative-beyond-top-level


class Workflow(Base):  # pylint: disable=too-few-public-methods
    """
    Workflow Model
    """
    __tablename__ = 'workflows'

    ResourceID = Column(String(38), primary_key=True)
    WorkflowName = Column(String(255), nullable=False)
    ParentID = Column(String(38), nullable=True)
    ResourceType = Column(Integer, nullable=True)
    CompletionState = Column(Integer, nullable=True)
    Notes = Column(Text, nullable=True)
    CreatedBy = Column(String(50), nullable=True)
    CreatedOn = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    ModifiedOn = Column(DateTime, nullable=True)
    LastModifiedOn = Column(DateTime, nullable=True)
    Version = Column(Integer, nullable=True)
    VersionDate = Column(DateTime, nullable=True)
    Empty = Column(Boolean, nullable=True)
    Enabled = Column(Boolean, nullable=True)
    Removed = Column(Boolean, nullable=True)
    ResultCode = Column(Integer, nullable=True)
    ResultText = Column(Text, nullable=True)
    StartedOn = Column(DateTime, nullable=True)
    EndedOn = Column(DateTime, nullable=True)
    LockedBy = Column(String(50), nullable=True)
    SuccessCount = Column(Integer, nullable=True)
    FailureCount = Column(Integer, nullable=True)
    NumberOfTasks = Column(Integer, nullable=True)
    UpdatedOn = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
