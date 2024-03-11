""" This module contains the schema for a workflow. """
from datetime import datetime
from pydantic import BaseModel


class TaskSchema(BaseModel):
    """

    :class:`TaskSchema`

    A class representing the schema for a workflow.

    """
    ID: str
    WorkflowID: str | None = None
    ResourceName: str | None = None
    ConstructTypeName: str | None = None
    ItemType: int | None = None
    ConstructID: str | None = None
    ConstructType: int | None = None
    Expression: str | None = None
    ResourceType: int | None = None
    CompletionState: int | None = None
    Notes: str | None = None
    CreatedBy: str | None = None
    CreatedOn: datetime | None = None
    ModifiedOn: datetime | None = None
    Version: int | None = None
    VersionDate: datetime | None = None
    Empty: bool | None = None
    Enabled: bool | None = None
    Removed: bool | None = None
    ResultCode: int | None = None
    ResultText: str | None = None
    StartedOn: datetime | None = None
    EndedOn: datetime | None = None
    LockedBy: str | None = None
    SuccessCount: int | None = None
    FailureCount: int | None = None
    RowLastUpdated: datetime | None = None

    class Config:  # pylint: disable=too-few-public-methods
        """A class representing the configuration for the ORM mode.

        Attributes:
            orm_mode (bool): A flag indicating whether the ORM mode is enabled or not.

        """
        orm_mode = True
