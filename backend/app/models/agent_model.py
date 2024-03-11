
"""
Agent Data Model
"""

import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from .base_model import Base  # pylint: disable=relative-beyond-top-level


class AgentData(Base):  # pylint: disable=too-few-public-methods
    """
    This is the agent class involving different details about a agent.
    Columns: AgentID, AgentName, GroupResourceID, GroupName, GroupParentID, Notes, CreatedOn, LastModifiedOn, Enabled  # pylint: disable=line-too-long
    """
    __tablename__ = 'agents'

    AgentID = Column(String(50), primary_key=True)
    AgentName = Column(String(150), nullable=True)
    GroupResourceID = Column(String(50), nullable=True)
    GroupName = Column(String(150), nullable=True)
    GroupParentID = Column(String(50), nullable=True)
    Notes = Column(String(500), nullable=True)
    CreatedOn = Column(DateTime, nullable=True)
    LastModifiedOn = Column(DateTime, nullable=True)
    Enabled = Column(Boolean, default=True)
    RowUpdated = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
