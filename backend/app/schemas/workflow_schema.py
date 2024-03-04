""" This module contains the schema for a workflow. """
import datetime
from pydantic import BaseModel


class WorkflowSchema(BaseModel):
    """

    :class:`WorkflowSchema`

    A class representing the schema for a workflow.

    Attributes:
        ResourceID (str): The ID of the resource.
        WorkflowName (str): The name of the workflow.
        ParentID (str): The ID of the parent.
        ResourceType (int): The type of the resource.
        CompletionState (int): The completion state of the workflow.
        Notes (str): Additional notes for the workflow.
        CreatedBy (str): The creator of the workflow.
        CreatedOn (datetime.datetime): The date and time when the workflow was created.
        ModifiedOn (datetime.datetime): The date and time when the workflow was modified.
        LastModifiedOn (datetime.datetime): The last date and time when the workflow was modified.
        Version (int): The version of the workflow.
        VersionDate (datetime.datetime): The date and time when the version of the workflow was created.  # pylint: disable=line-too-long
        Empty (int): The empty state of the workflow.
        Enabled (bool): The enabled state of the workflow.
        Removed (bool): The removed state of the workflow.
        ResultCode (int): The result code of the workflow.
        ResultText (str): The result text of the workflow.
        StartedOn (datetime.datetime): The date and time when the workflow was started.
        EndedOn (datetime.datetime): The date and time when the workflow was ended.
        LockedBy (str): The owner who has locked the workflow.
        SuccessCount (int): The count of successful tasks in the workflow.
        FailureCount (int): The count of failed tasks in the workflow.
        NumberOfTasks (int): The number of tasks in the workflow.
        UpdatedOn(datetime.datetime): The date and time when the workflow was last updated.

        Config (class):
            A nested class containing configuration settings for the class.

            Attributes:
                orm_mode (bool): Whether the class operates in an ORM mode.

    """
    ResourceID: str
    WorkflowName: str
    ParentID: str
    ResourceType: int
    CompletionState: int
    Notes: str
    CreatedBy: str
    CreatedOn: datetime.datetime
    ModifiedOn: datetime.datetime
    LastModifiedOn: datetime.datetime
    Version: int
    VersionDate: datetime.datetime
    Empty: int
    Enabled: bool
    Removed: bool
    ResultCode: int
    ResultText: str
    StartedOn: datetime.datetime
    EndedOn: datetime.datetime
    LockedBy: str
    SuccessCount: int
    FailureCount: int
    NumberOfTasks: int
    UpdatedOn: datetime.datetime

    class Config:  # pylint: disable=too-few-public-methods
        """A class representing the configuration for the ORM mode.

        Attributes:
            orm_mode (bool): A flag indicating whether the ORM mode is enabled or not.

        """
        orm_mode = True
