""" This module contains the schema for a agent. """
from datetime import datetime
from pydantic import BaseModel

class ServerSettingsChangeLogSchema(BaseModel):
    """" This is the automate server settings class involving
    different details about server settings."""

    RowID: int
    ID: str | None = None
    change_type: str | None = None
    global_triggering: int | None = None

    timestamp: datetime | None = None

    class Config:  # pylint: disable=too-few-public-methods
        """A nested class containing configuration settings for the class."""
        orm_mode = True
