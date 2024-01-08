"""
agent_data_model module

This module contains the Agent class which represents an agent resource in the system.

Classes:
    Agent: Represents an agent with multiple properties like resourceID, last_connectedID,
    last_connected_machinename and last_connect_datetime.

Dependencies:
    Packages: sqlalchemy, datetime
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Agent(Base):  # pylint: disable=too-few-public-methods
    """
    This is the Agent class involving different details about an agent.

    Attributes
    ----------
    id : int
        primary key, unique identifier for each agent
    resourceID : str
        unique identifier for the resource an agent is assigned to, can not be null
    last_connectedID : str
        identifier for the last connection made by agent, can not be null
    last_connected_machinename : str
        name of the machine agent last connected to, can not be null
    last_connect_datetime : DateTime
        time of the latest connection made by the agent, default is current UTC time

    """
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True)
    resourceID = Column(String(50), nullable=False)
    last_connectedID = Column(String(50), nullable=False)
    last_connected_machinename = Column(String(50), nullable=False)
    last_connect_datetime = Column(DateTime, default=datetime.datetime.utcnow)
