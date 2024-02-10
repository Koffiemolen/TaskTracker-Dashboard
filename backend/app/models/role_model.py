""" Role model """
from sqlalchemy import Column, Integer, String
from backend.app.models.base_model import Base  # pylint: disable=import-error

class Role(Base):  # pylint: disable=too-few-public-methods
    """
    Role model class. This class represents a table in the database with the name 'roles'.
    It has three columns: 'id', 'name', and 'description'.
    """
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
