
"""
Enriched Task Data Model
"""
from datetime import datetime
from pydantic import BaseModel


class TaskEnrichedSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """
    This is the TaskEnriched class involving different details about a task enriched with metadata.
    from agent and trigger
    """
    ID: str
    WorkflowID: str | None = None
    ResourceName: str | None = None
    ConstructTypeName: str | None = None
    TaskAgentID: str | None = None
    Enabled: bool | None = None
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
    Removed: bool | None = None
    ResultCode: int | None = None
    ResultText: str | None = None
    StartedOn: datetime | None = None
    EndedOn: datetime | None = None
    LockedBy: str | None = None
    SuccessCount: int | None = None
    FailureCount: int | None = None
    RowLastUpdated: datetime | None = None
    AgentID: str | None = None
    AgentName: str | None = None
    AgentGroupResourceID: str | None = None
    AgentGroupName: str | None = None
    AgentGroupParentID: str | None = None
    AgentNotes: str | None = None
    AgentCreatedOn: datetime | None = None
    AgentLastModifiedOn: datetime | None = None
    AgentEnabled: bool | None = None
    AgentRowUpdated: datetime | None = None
    TriggerID: str | None = None
    TriggerName: str | None = None
    TriggerType: str | None = None
    TriggerSource: str | None = None
    TriggerScheduleType: str | None = None
    TriggerLastLaunchDate: datetime | None = None
    TriggerNextLaunchDate: datetime | None = None
    TriggerFrequency: int | None = None
    TriggerRowUpdatedOn: datetime | None = None
