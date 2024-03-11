""" This module contains the schema for a trigger. """
from datetime import datetime
from pydantic import BaseModel

class TriggerSchema(BaseModel):
    """

    Module: TriggerSchema

    This module defines the class TriggerSchema, which is used to represent a trigger schema.

    :class:`TriggerSchema` class:
    ----------------------------------------
    This class is a subclass of `BaseModel` and represents a trigger schema.

    Attributes:
        - triggerID (str): The ID of the trigger.
        - triggerName (str, optional): The name of the trigger. Defaults to None.
        - triggerType (str): The type of the trigger.
        - source (str, optional): The source of the trigger. Defaults to None.
        - scheduleType (str, optional): The schedule type of the trigger. Defaults to None.
        - lastLaunchDate(datetime, optional): The last launch date of the trigger. Defaults to None.
        - nextLaunchDate(datetime, optional): The next launch date of the trigger. Defaults to None.
        - frequency (int, optional): The frequency of the trigger. Defaults to None.
        - rowUpdatedOn (datetime, optional): The row updated on date of the trigger. Defaults to None.  # pylint: disable=line-too-long

    Config:
        The `Config` subclass within `TriggerSchema` specifies configuration options.

        Attributes:
            - orm_mode (bool): Indicates whether the instance allows ORM mode or not. Defaults to True.  # pylint: disable=line-too-long

    Note:
        - This class is used to represent a trigger schema.

    Example usage:
        >>> trigger = TriggerSchema(triggerID='123', triggerName='Trigger1', triggerType='Type1')
        >>> trigger.triggerID
        '123'
        >>> trigger.triggerName
        'Trigger1'
        >>> trigger.triggerType
        'Type1'

    """

    triggerID: str
    triggerName: str | None = None
    triggerType: str
    source: str | None = None
    scheduleType: str | None = None
    lastLaunchDate: datetime | None = None
    nextLaunchDate: datetime | None = None
    frequency: int | None = None
    rowUpdatedOn: datetime | None = None

    class Config:  # pylint: disable=too-few-public-methods
        """A class representing the configuration for the ORM mode.

        Attributes:
            orm_mode (bool): A flag indicating whether the ORM mode is enabled or not.

        """
        orm_mode = True
