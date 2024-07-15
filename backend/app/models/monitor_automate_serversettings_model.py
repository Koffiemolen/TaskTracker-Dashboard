"""
Monitor Automate Server Settings Model
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .base_model import Base  # pylint: disable=relative-beyond-top-level

class ServerSettingsChangeLog(Base):  # pylint: disable=too-few-public-methods
    """
    This is the Task class involving details about a task.
    """
    __tablename__ = 'change_log_automate_server_settings'

    RowID = Column(Integer, primary_key=True)
    ID = Column(String(38))
    change_type = Column(String)
    global_triggering = Column(Integer)
    timestamp = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
