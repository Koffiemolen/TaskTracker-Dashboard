"""This module contains dependencies for user authentication and role-based access control."""
# backend/app/models/permission_model.py
from sqlalchemy import Column, Integer, String
from .base_model import Base # pylint: disable=relative-beyond-top-level

class Permission(Base):  # pylint: disable=too-few-public-methods
    """
    Permission model class. This class represents a table in the database with the name 'permissions'. # pylint: disable=line-too-long
    It has three columns: 'id', 'name', and 'description'.
    """
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
