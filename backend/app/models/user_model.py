"""
User model
"""
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from .base_model import Base


class User(Base):  # pylint: disable=too-few-public-methods
    """
    User Model
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    fullname = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # pylint: disable=line-too-long
    deleted = Column(Boolean, default=False)
    local_account = Column(Boolean, default=False)
