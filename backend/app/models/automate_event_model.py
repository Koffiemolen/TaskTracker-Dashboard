"""
Automate Event Model
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base_model import Base


class AutomateEvent(Base):  # pylint: disable=too-few-public-methods
    """
    Automate Event Model
    """
    __tablename__ = 'automate-events'

    id = Column(Integer, primary_key=True)
    eventID = Column(Integer, primary_key=True)
    event_date_time = Column(DateTime, default=datetime.datetime.utcnow)
    event_type = Column(Integer, nullable=False)
    event_description = Column(String(255), nullable=True)
    user_id = Column(String(50), nullable=False)
    primary_constructID = Column(String(50), nullable=False)
