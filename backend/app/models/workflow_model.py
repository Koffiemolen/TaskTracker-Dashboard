"""
Workflow Model
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Workflow(Base):  # pylint: disable=too-few-public-methods
    """
    Workflow Model
    """
    __tablename__ = 'workflows'

    id = Column(Integer, primary_key=True)
    instanceID = Column(Integer, nullable=False)
    WorkflowID = Column(String(50), nullable=False)
    fullname = Column(String(255), nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Integer, nullable=True)
    result_code = Column(Integer, nullable=True)
    automate_userID = Column(String(50), nullable=False)
