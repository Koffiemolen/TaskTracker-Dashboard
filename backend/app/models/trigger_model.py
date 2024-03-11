"""
Trigger Model
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base_model import Base  # pylint: disable=relative-beyond-top-level


class Trigger(Base):  # pylint: disable=too-few-public-methods
    """
    Trigger Model
    """
    __tablename__ = 'triggers'

    triggerID = Column(String(38), primary_key=True)
    triggerName = Column(String(255), nullable=True)
    triggerType = Column(String(100), nullable=False)
    source = Column(String(500), nullable=True)
    scheduleType = Column(String(50), nullable=True)
    lastLaunchDate = Column(DateTime, nullable=True)
    nextLaunchDate = Column(DateTime, nullable=True)
    frequency = Column(Integer, nullable=True)
    rowUpdatedOn = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    