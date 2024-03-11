""" This module contains the schema for a agent. """
from datetime import datetime
from pydantic import BaseModel


class AgentSchema(BaseModel):
    """" This is the agent class involving different details about a agent."""

    AgentID: str
    AgentName: str | None = None
    GroupResourceID: str | None = None
    GroupName: str | None = None
    GroupParentID: str | None = None
    Notes: str | None = None
    CreatedOn: datetime | None = None
    LastModifiedOn: datetime | None = None
    Enabled: bool
    RowUpdated: datetime | None = None

    class Config:  # pylint: disable=too-few-public-methods
        """A nested class containing configuration settings for the class."""
        orm_mode = True
