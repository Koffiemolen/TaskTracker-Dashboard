"""
Module Docstring:

This module contains the `DataAggregationService` class used for handling data aggregation tasks.

Classes:
    - `DataAggregationService`: This class handles various operations related to data aggregation.

      Attributes:
        - `target_engine`: This attribute tracks the target engine for data aggregation.
        - `source_session_local`: This attribute manages the source session for local data aggregation.  # pylint: disable=line-too-long
        - `source_engine`: This attribute tracks the source engine for data aggregation.
        - `target_session_local`: This attribute manages the target session for local data aggregation.  # pylint: disable=line-too-long

      Methods:
        - `__init__`: This method initializes the `DataAggregationService` attributes.
        - `transfer_data`: This method handles the transfer of aggregated data.
        - `_sync_transfer_data`: This is a private method which syncs the data transfer.

Note: This module is a part of a larger system, and usage should conform to that wider architecture.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.concurrency import run_in_threadpool


class DataAggregationService:  # pylint: disable=too-few-public-methods
    """`DataAggregationService`: This class handles various operations related to data aggregation."""  # pylint: disable=line-too-long

    def __init__(self, source_db_url: str, target_db_url: str):
        self.source_engine = create_engine(source_db_url)
        self.target_engine = create_engine(target_db_url)

        # Create a sessionmaker for each engine
        self.source_session_local = sessionmaker(autocommit=False, autoflush=False,
                                                 bind=self.source_engine)  # pylint: disable=line-too-long
        self.target_session_local = sessionmaker(autocommit=False, autoflush=False,
                                                 bind=self.target_engine)  # pylint: disable=line-too-long

    async def transfer_data_workflow(self):
        """This method handles the transfer of aggregated data."""
        # SQL statement on 1 line
        # transfer_sql = "INSERT INTO [TaskTracker].[dbo].[workflows] (ResourceID,WorkflowName,ParentID,ResourceType,CompletionState,Notes,CreatedBy,CreatedOn,ModifiedOn,LastModifiedOn,Version,VersionDate,Empty,Enabled,Removed,ResultCode,ResultText,StartedOn,EndedOn,LockedBy,SuccessCount,FailureCount,NumberOfTasks) SELECT ac.ResourceID,ac.ResourceName,ac.ParentID,ac.ResourceType,ac.CompletionState,ac.Notes,ac.CreatedBy,ac.CreatedOn,ac.ModifiedOn,ac.LastModifiedOn,ac.Version,ac.VersionDate,ac.Empty,ac.Enabled,ac.Removed,ac.ResultCode,ac.ResultText,ac.StartedOn,ac.EndedOn,ac.LockedBy,ac.SuccessCount,ac.FailureCount,(SELECT COUNT(*) FROM [Automate11].[dbo].[workflowitemconstructs] wic WHERE wic.WorkflowID = ac.ResourceID) AS NumberOfTasks FROM [Automate11].[dbo].[automateconstructs] ac WHERE ac.ResourceType = 3;"  # pylint: disable=line-too-long

        transfer_sql = text("""WITH WorkflowData AS (
    SELECT
        ac.ResourceID,
        MAX(stc.NextLaunchDate) AS NextLaunchDate,
        MAX(stc.LastLaunchDate) AS LastLaunchDate,
        COUNT(DISTINCT wic.ConstructID) AS NumberOfTasks -- Assuming ConstructID uniquely identifies tasks
    FROM [Automate11].[dbo].[automateconstructs] ac
    LEFT JOIN [Automate11].[dbo].[workflowitemconstructs] wic ON ac.ResourceID = wic.WorkflowID
    LEFT JOIN [Automate11].[dbo].[scheduletriggerconstructs] stc ON wic.ConstructID = stc.ResourceID
    WHERE ac.ResourceType = 3
    GROUP BY ac.ResourceID
)
MERGE INTO [TaskTracker].[dbo].[workflows] AS target
USING (
    SELECT 
        ac.ResourceID,
        ac.ResourceName,
        ac.ParentID,
        ac.ResourceType,
        ac.CompletionState,
        ac.Notes,
        ac.CreatedBy,
        ac.CreatedOn,
        ac.ModifiedOn,
        ac.LastModifiedOn,
        ac.Version,
        ac.VersionDate,
        ac.Empty,
        ac.Enabled,
        ac.Removed,
        ac.ResultCode,
        ac.ResultText,
        ac.StartedOn,
        ac.EndedOn,
        ac.LockedBy,
        ac.SuccessCount,
        ac.FailureCount,
        wd.NumberOfTasks,
        wd.NextLaunchDate,
        wd.LastLaunchDate
    FROM [Automate11].[dbo].[automateconstructs] ac
    JOIN WorkflowData wd ON ac.ResourceID = wd.ResourceID
    WHERE ac.ResourceType = 3
) AS source
ON target.ResourceID = source.ResourceID

-- For Inserts
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ResourceID, WorkflowName, ParentID, ResourceType, CompletionState, Notes, CreatedBy, CreatedOn, ModifiedOn, LastModifiedOn, Version, VersionDate, Empty, Enabled, Removed, ResultCode, ResultText, StartedOn, EndedOn, LockedBy, SuccessCount, FailureCount, NumberOfTasks, NextLaunchDate, LastLaunchDate, UpdatedOn)
    VALUES (source.ResourceID, source.ResourceName, source.ParentID, source.ResourceType, source.CompletionState, source.Notes, source.CreatedBy, source.CreatedOn, source.ModifiedOn, source.LastModifiedOn, source.Version, source.VersionDate, source.Empty, source.Enabled, source.Removed, source.ResultCode, source.ResultText, source.StartedOn, source.EndedOn, source.LockedBy, source.SuccessCount, source.FailureCount, source.NumberOfTasks, source.NextLaunchDate, source.LastLaunchDate, GETDATE())

-- For Updates
WHEN MATCHED AND (
    target.WorkflowName <> source.ResourceName OR
    target.ParentID <> source.ParentID OR
    target.CompletionState <> source.CompletionState OR
    CAST(target.Notes AS NVARCHAR(MAX)) <> CAST(source.Notes AS NVARCHAR(MAX)) OR
    target.ModifiedOn <> source.ModifiedOn OR
    target.LastModifiedOn <> source.LastModifiedOn OR
    target.Version <> source.Version OR
    target.VersionDate <> source.VersionDate OR
    target.Enabled <> source.Enabled OR
    target.Removed <> source.Removed OR
    target.ResultCode <> source.ResultCode OR
	CAST(target.ResultText AS NVARCHAR(MAX)) <> CAST(source.ResultText AS NVARCHAR(MAX)) OR
    target.StartedOn <> source.StartedOn OR
    target.EndedOn <> source.EndedOn OR
    target.LockedBy <> source.LockedBy OR
    target.SuccessCount <> source.SuccessCount OR
    target.FailureCount <> source.FailureCount OR
    target.NumberOfTasks <> source.NumberOfTasks OR
	target.NextLaunchDate <> source.NextLaunchDate OR
	target.LastLaunchDate <> source.LastLaunchDate
)THEN
    UPDATE SET
        target.WorkflowName = source.ResourceName,
        target.ParentID = source.ParentID,
        target.CompletionState = source.CompletionState,
        target.Notes = source.Notes,
        target.ModifiedOn = source.ModifiedOn,
        target.LastModifiedOn = source.LastModifiedOn,
        target.Version = source.Version,
        target.VersionDate = source.VersionDate,
        target.Enabled = source.Enabled,
        target.Removed = source.Removed,
        target.ResultCode = source.ResultCode,
        target.ResultText = source.ResultText,
        target.StartedOn = source.StartedOn,
        target.EndedOn = source.EndedOn,
        target.LockedBy = source.LockedBy,
        target.SuccessCount = source.SuccessCount,
        target.FailureCount = source.FailureCount,
        target.NumberOfTasks = source.NumberOfTasks,
        target.NextLaunchDate = source.NextLaunchDate,
        target.LastLaunchDate = source.LastLaunchDate,
        target.UpdatedOn = GETDATE()

-- For Delete
WHEN NOT MATCHED BY source THEN
	DELETE
;
""")

        # Execute the transfer using run_in_threadpool for synchronous operations
        await run_in_threadpool(self._sync_transfer_data, transfer_sql)

    async def transfer_data_agents(self):
        """Transfers data for the agents."""
        transfer_sql = text("""WITH AgentGroups AS (
    -- Existing CTE that identifies agents with groups
    SELECT
        CAST(agc.AgentIDs AS nvarchar(MAX)) AS AgentIDs,
        agc.ResourceID as GroupResourceID,
        ac.ResourceName as GroupName,
        ac.ParentID as GroupParentID
    FROM [Automate11].[dbo].[agentgroupconstructs] agc
    LEFT JOIN [Automate11].[dbo].[automateconstructs] ac
        ON ac.ResourceID = agc.ResourceID AND ac.ResourceType = 11
),
SplitAgents AS (
    SELECT
        value as AgentID,
        GroupResourceID,
        GroupName,
        GroupParentID
    FROM AgentGroups
    CROSS APPLY STRING_SPLIT(AgentIDs, ';')
    WHERE LTRIM(RTRIM(value)) != ''
),
Agents AS (
    SELECT
        ac.ResourceID as AgentID,
        ac.ResourceName as AgentName,
        ac.Notes,
        ac.CreatedOn,
        ac.LastModifiedOn,
        ac.Enabled
    FROM [Automate11].[dbo].[automateconstructs] ac
    WHERE ac.ResourceType = 8
),
AgentDataComplete AS (
    SELECT
        a.AgentID,
        a.AgentName,
        sa.GroupResourceID,
        sa.GroupName,
        sa.GroupParentID,
        a.Notes,
        a.CreatedOn,
        a.LastModifiedOn,
        a.Enabled
    FROM Agents a
    LEFT JOIN SplitAgents sa ON a.AgentID = sa.AgentID
)

MERGE INTO [TaskTracker].[dbo].[agents] AS target
USING (
	SELECT AgentID, AgentName, GroupResourceID, GroupName, GroupParentID, Notes, CreatedOn, LastModifiedOn, Enabled FROM AgentDataComplete
) AS source 
ON target.AgentID = source.AgentID

-- For Inserts
WHEN NOT MATCHED BY TARGET THEN
    INSERT (AgentID, AgentName, GroupResourceID, GroupName, GroupParentID, Notes, CreatedOn, LastModifiedOn, Enabled)
    VALUES (source.AgentID, source.AgentName, source.GroupResourceID, source.GroupName, source.GroupParentID, source.Notes, source.CreatedOn, source.LastModifiedOn, source.Enabled)

-- For Updates
WHEN MATCHED AND (
	target.AgentName <> source.AgentName OR
        target.GroupResourceID <> source.GroupResourceID OR
        target.GroupName <> source.GroupName OR
        target.GroupParentID <> source.GroupParentID OR
        CAST(target.Notes AS NVARCHAR(MAX)) <> CAST(source.Notes AS NVARCHAR(MAX)) OR
        target.CreatedOn <> source.CreatedOn OR
        target.LastModifiedOn <> source.LastModifiedOn OR
        target.Enabled <> source.Enabled
) THEN
    UPDATE SET
        target.AgentName = source.AgentName,
        target.GroupResourceID = source.GroupResourceID,
        target.GroupName = source.GroupName,
        target.GroupParentID = source.GroupParentID,
        target.Notes = source.Notes,
        target.CreatedOn = source.CreatedOn,
        target.LastModifiedOn = source.LastModifiedOn,
        target.Enabled = source.Enabled

-- For Delete
WHEN NOT MATCHED BY source THEN
	DELETE
;
""")

        # Execute the transfer using run_in_threadpool for synchronous operations
        await run_in_threadpool(self._sync_transfer_data, transfer_sql)

    async def transfer_data_triggers(self):
        """Transfers data for the triggers."""
        transfer_sql = text("""MERGE INTO [TaskTracker].[dbo].[triggers] AS target
USING (
	SELECT [TriggerID]
      ,[TriggerName]
      ,[TriggerType]
      ,[Source]
      ,[ScheduleType]
      ,[LastLaunchDate]
      ,[NextLaunchDate]
      ,[Frequency]
  FROM [Automate11].[dbo].[ConsolidatedTriggerInfo]

) AS source 
ON target.triggerID = source.TriggerID

-- For Inserts
WHEN NOT MATCHED BY TARGET THEN
    INSERT ([TriggerID]
      ,[TriggerName]
      ,[TriggerType]
      ,[Source]
      ,[ScheduleType]
      ,[LastLaunchDate]
      ,[NextLaunchDate]
      ,[Frequency])
    VALUES (source.[TriggerID], source.[TriggerName], source.[TriggerType], source.[Source], source.[ScheduleType], source.[LastLaunchDate], source.[NextLaunchDate], source.[Frequency])

-- For Updates
WHEN MATCHED AND (
	target.[TriggerName] <> source.[TriggerName] OR
        target.[TriggerType] <> source.[TriggerType] OR
        target.[Source] <> source.[Source] OR
        target.[ScheduleType] <> source.[ScheduleType] OR
        target.[LastLaunchDate] <> source.[LastLaunchDate] OR
        target.[NextLaunchDate] <> source.[NextLaunchDate] OR
        target.[Frequency] <> source.[Frequency]
) THEN
    UPDATE SET
        target.[TriggerName] = source.[TriggerName],
        target.[TriggerType] = source.[TriggerType],
        target.[Source] = source.[Source],
        target.[ScheduleType] = source.[ScheduleType],
        target.[LastLaunchDate] = source.[LastLaunchDate],
        target.[NextLaunchDate] = source.[NextLaunchDate],
        target.[Frequency] = source.[Frequency]

-- For Delete
WHEN NOT MATCHED BY source THEN
	DELETE
;
""")

        # Execute the transfer using run_in_threadpool for synchronous operations
        await run_in_threadpool(self._sync_transfer_data, transfer_sql)

    def _sync_transfer_data(self, sql_statement):
        """Synchronizes the transfer of data."""
        with self.target_session_local() as session:
            session.execute(sql_statement)
            session.commit()
