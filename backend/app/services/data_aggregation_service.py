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
"""
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.concurrency import run_in_threadpool
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from backend.app.websocket_manager import manager  # pylint: disable=import-error
from backend.app.models.monitor_automate_serversettings_model import ServerSettingsChangeLog  # pylint: disable=import-error
from backend.app.schemas.monitor_automate_serversettings_schema import ServerSettingsChangeLogSchema  # pylint: disable=import-error

class ServerSettingsChangeLogSchema(SQLAlchemyAutoSchema):  # pylint: disable=too-few-public-methods, function-redefined
    """ Fancy docstring here"""
    class Meta:  # pylint: disable=too-few-public-methods
        """ tada """
        model = ServerSettingsChangeLog
        load_instance = True


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

    # Adjusting the coroutine to run once per invocation
    async def monitor_table_changes(self):
        """Checks for new rows in the table once and sends notifications."""
        last_checked_time = datetime.now() - timedelta(seconds=5)  # Adjust according to your needs
        # Assuming last_checked_time is stored in a way that persists between invocations
        with self.source_session_local() as session:
            result = session.execute(
                # text("SELECT * FROM [TaskTracker].[dbo].[change_log_automate_server_settings] WHERE global_triggering = 0 AND timestamp > :last_checked_time"),
                # {"last_checked_time": last_checked_time}
                text(
                    "SELECT * FROM [TaskTracker].[dbo].[change_log_automate_server_settings] WHERE timestamp > :last_checked_time"),
                {"last_checked_time": last_checked_time}
            )
            new_rows = result.mappings().all()
            # print(f"new_rows before if statement: {new_rows}")
            if new_rows:
                # Update the last_checked_time based on the latest timestamp from new_rows
                last_checked_time = max(row['timestamp'] for row in new_rows)
                # print(f"converting rows {new_rows}")

                # Adjust the schema usage to handle multiple items
                schema = ServerSettingsChangeLogSchema(many=True)  # Set many=True here
                output = schema.dump(new_rows, many=True)

                # Directly using output for JSON serialization
                json_output = json.dumps(output)  # This is already JSON compatible

                # Construct the WebSocket message
                message = {
                    "type": "server_settings_change",
                    "data": json_output  # Use the output directly, which is already a list of dicts
                }

                print(f"final message: {message}")

                # Serialize the entire message, not just the output
                json_message = json.dumps(message)
                print(f"final json message: {json_message}")
                # Send the message over an established WebSocket connection
                # await self.notify_clients(message)
                # Send the message over an established WebSocket connection
                await manager.broadcast(json_message, 'globaltriggering')
                print("Broadcasted global triggering updates to channel 'globaltriggering' ")

    async def notify_clients(self, message):
        """Convert message to JSON string here if not already"""
        json_message = json.dumps(message) if not isinstance(message, str) else message
        print(f"New changes detected: {json_message}.")
        await manager.broadcast(json_message)

    def _sync_transfer_data(self, sql_statement):
        """Synchronizes the transfer of data."""
        with self.target_session_local() as session:
            session.execute(sql_statement)
            session.commit()

    def fetch_new_or_updated_workflows(self):
        """Checks for new rows in the table once and sends notifications."""
        last_checked_time = datetime.now() - timedelta(seconds=10)
        # Assuming last_checked_time is stored in a way that persists between invocations
        with self.source_session_local() as session:
            result = session.execute(
                text(
                    "SELECT * FROM [TaskTracker].[dbo].[workflows] WHERE [UpdatedOn] > :last_checked_time"),
                {"last_checked_time": last_checked_time}
            )
            workflows = result.mappings().all()
            # print(f"workflows before if statement: {workflows}")

            return workflows

    def _serialize_workflow(self, workflow):
        # Convert SQLAlchemy model instance to a dictionary for JSON serialization
        return {
            "ResourceID": workflow.ResourceID,
            "WorkflowName": workflow.WorkflowName,
            "CompletionState": workflow.CompletionState,
            "Notes": workflow.Notes,
            "LastModifiedOn": workflow.LastModifiedOn,
            "Version": workflow.Version,
            "VersionDate": workflow.VersionDate,
            "Enabled": workflow.Enabled,
            "Removed": workflow.Removed,
            "ResultCode": workflow.ResultCode,
            "ResultText": workflow.ResultText,
            "StartedOn": workflow.StartedOn,
            "EndedOn": workflow.EndedOn,
            "NumberOfTasks": workflow.NumberOfTasks,
            "NextLaunchDate": workflow.NextLaunchDate,
            "LastLaunchDate": workflow.LastLaunchDate,
            "UpdatedOn": workflow.UpdatedOn.isoformat() if workflow.UpdatedOn else None
        }

    async def check_for_workflow_update(self):
        """ updating delta to ws channel"""
        new_or_updated_workflows = self.fetch_new_or_updated_workflows()
        if new_or_updated_workflows:
            print(f"TADAAAAAAAAAA {len(new_or_updated_workflows)} new/updated workflows.")

            # Serialize the workflows to JSON
            try:
                message_data = json.dumps(new_or_updated_workflows,
                                          default=str)  # Using default=str to handle most non-serializable types
            except TypeError as e:
                print(f"Error serializing workflows: {e}")
                return

            # Construct the WebSocket message
            message = {
                "type": "workflow_update",
                "data": message_data
            }
            json_message = json.dumps(message)

            # Send the message over an established WebSocket connection
            await manager.broadcast(json_message, 'workflow_updates')
            print("Broadcasted workflow updates to channel 'workflow_updates' ")


    async def emit_workflow_updates(self, workflows, group=None):
        """ todoo """
        if workflows:  # Check if there are any updates to send
            message = {"type": "workflow_update", "data": workflows}
            # Call the generic emit method with optional group targeting
            await self.emit(message, group=group)

    async def emit(self, message, group=None):
        """Convert message to JSON if it's not a string"""
        if not isinstance(message, str):
            message = json.dumps(message)
        # Use the WebSocket manager to broadcast the message
        await manager.broadcast(message, group=group)

    def fetch_new_or_updated_tasks(self):
        """Checks for new rows in the table once and sends notifications."""
        last_checked_time = datetime.now() - timedelta(seconds=10)

        with self.source_session_local() as session:
            result = session.execute(
                text(
                    "SELECT * FROM [TaskTracker].[dbo].[tasks] WHERE [RowLastUpdated] > :last_checked_time"),
                {"last_checked_time": last_checked_time}
            )
            tasks = result.mappings().all()
            print(f"fetch_new_or_updated_tasks - tasks before if statement: {tasks}")

            return tasks
    async def check_for_task_update(self):
        """ sending tasks deltas"""
        print("check_for_task_update - Looking for new tasks")
        new_or_updated_tasks = self.fetch_new_or_updated_tasks()

        print("check_for_task_update - check if new_or_updated_tasks contains someting")
        if new_or_updated_tasks:
            print("check_for_task_update - new tasks present")
            # Serialize the tasks to JSON. Adjust this if your data structure requires.
            try:
                message_data = json.dumps(new_or_updated_tasks,
                                          default=str)  # Using default=str to handle most non-serializable types
            except TypeError as e:
                print(f"Error serializing tasks: {e}")
                return

            # Construct the WebSocket message
            message = {
                "type": "task_updates",
                "data": message_data
            }
            json_message = json.dumps(message)

            # Send the message over an established WebSocket connection
            print(f"check_for_task_update - sending tasks: {json_message}")
            await manager.broadcast(json_message, 'task_updates')
            print("check_for_task_update - Broadcasted task updates to channel 'task_updates' ")
        else:
            print("No new tasks present")

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

    async def transfer_data_tasks(self):
        """Transfers data for the tasks."""
        transfer_sql = text("""MERGE INTO [TaskTracker].[dbo].[tasks] AS target
USING (
    SELECT 
        wic.ID,
        wic.WorkflowID,
        ac.ResourceName,
        CASE 
            WHEN wic.ConstructType = 2 THEN 'Task'
            WHEN wic.ConstructType = 4 THEN 'Trigger'
            WHEN wic.ConstructType = 19 THEN 'Wait'
            WHEN wic.ConstructType = 13 THEN 'Evaluation'
            ELSE CAST(wic.ConstructType AS NVARCHAR(20))
        END AS ConstructTypeName,
        wic.AgentID,
        wic.ItemType,
        wic.ConstructID,
        wic.ConstructType,
        wic.Expression,
        ac.ResourceType,
        ac.CompletionState,
        ac.Notes,
        ac.CreatedBy,
        ac.CreatedOn,
        ac.ModifiedOn,
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
        ac.FailureCount
    FROM [Automate11].[dbo].[workflowitemconstructs] wic
    LEFT JOIN [Automate11].[dbo].[automateconstructs] ac ON ac.ResourceID = wic.ConstructID
) AS source
ON target.ID = source.ID -- or the appropriate key for matching

-- For Inserts
WHEN NOT MATCHED BY TARGET THEN
    INSERT (ID, WorkflowID, ResourceName, ConstructTypeName, AgentID, ItemType, ConstructID, ConstructType, Expression, ResourceType, CompletionState, Notes, CreatedBy, CreatedOn, ModifiedOn, Version, VersionDate, Empty, Enabled, Removed, ResultCode, ResultText, StartedOn, EndedOn, LockedBy, SuccessCount, FailureCount)
    VALUES (source.ID, source.WorkflowID, source.ResourceName, source.ConstructTypeName, source.AgentID, source.ItemType, source.ConstructID, source.ConstructType, source.Expression, source.ResourceType, source.CompletionState, source.Notes, source.CreatedBy, source.CreatedOn, source.ModifiedOn, source.Version, source.VersionDate, source.Empty, source.Enabled, source.Removed, source.ResultCode, source.ResultText, source.StartedOn, source.EndedOn, source.LockedBy, source.SuccessCount, source.FailureCount)

-- For Updates (adjust conditions as needed)
WHEN MATCHED AND (
		target.WorkflowID <> source.WorkflowID or
		target.ResourceName <> source.ResourceName or
		target.ConstructTypeName <> source.ConstructTypeName or
		target.ItemType <> source.ItemType or
		target.ConstructID <> source.ConstructID or
		target.ConstructType <> source.ConstructType or
		target.AgentID <> source.AgentID or
		target.Expression <> source.Expression or
		target.ResourceType <> source.ResourceType or
		target.CompletionState <> source.CompletionState or
		CAST(target.Notes AS NVARCHAR(MAX)) <> CAST(source.Notes AS NVARCHAR(MAX)) OR
		target.CreatedBy <> source.CreatedBy or
		target.CreatedOn <> source.CreatedOn or
		target.ModifiedOn <> source.ModifiedOn or
		target.Version <> source.Version or
		target.VersionDate <> source.VersionDate or
		target.Empty <> source.Empty or
		target.Enabled <> source.Enabled or
		target.Removed <> source.Removed or
		target.ResultCode <> source.ResultCode or
		CAST(target.ResultText AS NVARCHAR(MAX)) <> CAST(source.ResultText AS NVARCHAR(MAX)) OR
		target.StartedOn <> source.StartedOn or
		target.EndedOn <> source.EndedOn or
		target.LockedBy <> source.LockedBy or
		target.SuccessCount <> source.SuccessCount or
		target.FailureCount <> source.FailureCount
)THEN 
    UPDATE SET
		target.WorkflowID = source.WorkflowID,
		target.ResourceName = source.ResourceName,
		target.ConstructTypeName = source.ConstructTypeName,
		target.ItemType = source.ItemType,
		target.ConstructID = source.ConstructID,
		target.ConstructType = source.ConstructType,
		target.AgentID = source.AgentID,
		target.Expression = source.Expression,
		target.ResourceType = source.ResourceType,
		target.CompletionState = source.CompletionState,
		target.Notes = source.Notes,
		target.CreatedBy = source.CreatedBy,
		target.CreatedOn = source.CreatedOn,
		target.ModifiedOn = source.ModifiedOn,
		target.Version = source.Version,
		target.VersionDate = source.VersionDate,
		target.Empty = source.Empty,
		target.Enabled = source.Enabled,
		target.Removed = source.Removed,
		target.ResultCode = source.ResultCode,
		target.ResultText = source.ResultText,
		target.StartedOn = source.StartedOn,
		target.EndedOn = source.EndedOn,
		target.LockedBy = source.LockedBy,
		target.SuccessCount = source.SuccessCount,
		target.FailureCount = source.FailureCount,
		target.RowLastUpdated = GETDATE()

-- For Delete (if applicable)
WHEN NOT MATCHED BY SOURCE THEN
    DELETE
;
""")

        # Execute the transfer using run_in_threadpool for synchronous operations
        await run_in_threadpool(self._sync_transfer_data, transfer_sql)


    async def transfer_automate_server_settings(self):
        """Transfers data for the server settings."""
        transfer_sql = text(""" MERGE INTO [TaskTracker].[dbo].[automateserversettings] AS target
USING (
	SELECT [ID]
      ,[UseIPFilters]
      ,[BlockListType]
      ,[BlockedIPList]
      ,[DefaultIPFiltersAllow]
      ,[UseSSL]
      ,[CertStoreLocation]
      ,[CertStoreName]
      ,[CertSearchType]
      ,[CertSearchValue]
      ,[SMTPServer]
      ,[SMTPPort]
      ,[SMTPUser]
      ,[SMTPPassword]
      ,[ErrorNotifyEmailToAddress]
      ,[ErrorNotifyEmailFromAddress]
      ,[ErrorRunTaskName]
      ,[UseLowestCompletionState]
      ,[LowestCompletionState]
      ,[TrimTimeFrame]
      ,[TrimCount]
      ,[InstancesTrimTimeFrame]
      ,[InstancesTrimCount]
      ,[TaskStepsTrimTimeFrame]
      ,[TaskStepsTrimCount]
      ,[MaxRunningWorkflows]
      ,[WorkflowDelayAfterStartup]
      ,[DefaultStaging]
      ,[Versioned]
      ,[VersionBehavior]
      ,[VersionTrimValue]
      ,[GlobalTriggering]
      ,[EnableLockout]
      ,[LockoutPeriod]
      ,[AttemptPeriod]
      ,[AttemptCount]
      ,[EnableTimeout]
      ,[TimeoutPeriod]
      ,[TimeoutUserIDs]
      ,[DisableConcurrentLogin]
      ,[EnableAPI]
      ,[EnableStepLogging]
      ,[AuditEventsTrimTimeFrame]
      ,[AuditEventsTrimCount]
      ,[PCMMinimumLength]
      ,[PCMAllowLowercase]
      ,[PCMMinimumLowercase]
      ,[PCMAllowUppercase]
      ,[PCMMinimumUppercase]
      ,[PCMAllowNumbers]
      ,[PCMMinimumNumbers]
      ,[PCMAllowSpecCharacters]
      ,[PCMMinimumSpecCharacters]
      ,[PCMEnablePasswordExpiration]
      ,[PCMPasswordExpirationPeriod]
      ,[PCMEnablePasswordHistory]
      ,[PCMEnforcePasswordHistory]
      ,[EnableCustomActions]
  FROM [Automate11].[dbo].[serverproperties]
) AS source 
ON target.ID = source.ID

-- For Inserts
WHEN NOT MATCHED BY TARGET THEN
    INSERT ([ID]
      ,[UseIPFilters]
      ,[BlockListType]
      ,[BlockedIPList]
      ,[DefaultIPFiltersAllow]
      ,[UseSSL]
      ,[CertStoreLocation]
      ,[CertStoreName]
      ,[CertSearchType]
      ,[CertSearchValue]
      ,[SMTPServer]
      ,[SMTPPort]
      ,[SMTPUser]
      ,[SMTPPassword]
      ,[ErrorNotifyEmailToAddress]
      ,[ErrorNotifyEmailFromAddress]
      ,[ErrorRunTaskName]
      ,[UseLowestCompletionState]
      ,[LowestCompletionState]
      ,[TrimTimeFrame]
      ,[TrimCount]
      ,[InstancesTrimTimeFrame]
      ,[InstancesTrimCount]
      ,[TaskStepsTrimTimeFrame]
      ,[TaskStepsTrimCount]
      ,[MaxRunningWorkflows]
      ,[WorkflowDelayAfterStartup]
      ,[DefaultStaging]
      ,[Versioned]
      ,[VersionBehavior]
      ,[VersionTrimValue]
      ,[GlobalTriggering]
      ,[EnableLockout]
      ,[LockoutPeriod]
      ,[AttemptPeriod]
      ,[AttemptCount]
      ,[EnableTimeout]
      ,[TimeoutPeriod]
      ,[TimeoutUserIDs]
      ,[DisableConcurrentLogin]
      ,[EnableAPI]
      ,[EnableStepLogging]
      ,[AuditEventsTrimTimeFrame]
      ,[AuditEventsTrimCount]
      ,[PCMMinimumLength]
      ,[PCMAllowLowercase]
      ,[PCMMinimumLowercase]
      ,[PCMAllowUppercase]
      ,[PCMMinimumUppercase]
      ,[PCMAllowNumbers]
      ,[PCMMinimumNumbers]
      ,[PCMAllowSpecCharacters]
      ,[PCMMinimumSpecCharacters]
      ,[PCMEnablePasswordExpiration]
      ,[PCMPasswordExpirationPeriod]
      ,[PCMEnablePasswordHistory]
      ,[PCMEnforcePasswordHistory]
      ,[EnableCustomActions]
	  ,[RowLastUpdated])
    VALUES (source.[ID],source.[UseIPFilters],source.[BlockListType] ,source.[BlockedIPList] ,source.[DefaultIPFiltersAllow]
      ,source.[UseSSL] ,source.[CertStoreLocation] ,source.[CertStoreName] ,source.[CertSearchType] ,source.[CertSearchValue]
      ,source.[SMTPServer] ,source.[SMTPPort] ,source.[SMTPUser] ,source.[SMTPPassword] ,source.[ErrorNotifyEmailToAddress]
      ,source.[ErrorNotifyEmailFromAddress] ,source.[ErrorRunTaskName] ,source.[UseLowestCompletionState] ,source.[LowestCompletionState]
      ,source.[TrimTimeFrame] ,source.[TrimCount] ,source.[InstancesTrimTimeFrame] ,source.[InstancesTrimCount] ,source.[TaskStepsTrimTimeFrame] ,source.[TaskStepsTrimCount]
      ,source.[MaxRunningWorkflows] ,source.[WorkflowDelayAfterStartup] ,source.[DefaultStaging] ,source.[Versioned]
      ,source.[VersionBehavior] ,source.[VersionTrimValue] ,source.[GlobalTriggering] ,source.[EnableLockout] ,source.[LockoutPeriod]
      ,source.[AttemptPeriod] ,source.[AttemptCount] ,source.[EnableTimeout] ,source.[TimeoutPeriod] ,source.[TimeoutUserIDs]
      ,source.[DisableConcurrentLogin] ,source.[EnableAPI] ,source.[EnableStepLogging] ,source.[AuditEventsTrimTimeFrame] ,source.[AuditEventsTrimCount]
      ,source.[PCMMinimumLength] ,source.[PCMAllowLowercase] ,source.[PCMMinimumLowercase] ,source.[PCMAllowUppercase] ,source.[PCMMinimumUppercase]
      ,source.[PCMAllowNumbers] ,source.[PCMMinimumNumbers] ,source.[PCMAllowSpecCharacters] ,source.[PCMMinimumSpecCharacters]
      ,source.[PCMEnablePasswordExpiration] ,source.[PCMPasswordExpirationPeriod] ,source.[PCMEnablePasswordHistory] ,source.[PCMEnforcePasswordHistory]
      ,source.[EnableCustomActions] ,GETDATE()
	  )

-- For Updates
WHEN MATCHED AND (
	target.[GlobalTriggering] <> source.[GlobalTriggering]
) THEN
    UPDATE SET
        target.[GlobalTriggering] = source.[GlobalTriggering],
		[RowLastUpdated] = GETDATE()

-- For Delete
WHEN NOT MATCHED BY source THEN
	DELETE

OUTPUT inserted.ID, $action, inserted.GlobalTriggering INTO [TaskTracker].[dbo].[change_log_automate_server_settings] (ID, change_type, global_triggering)
;
""")
        # Execute the transfer using run_in_threadpool for synchronous operations
        print("running transfer data")
        await run_in_threadpool(self._sync_transfer_data, transfer_sql)

    def _sync_transfer_data(self, sql_statement):
        """Synchronizes the transfer of data."""
        with self.target_session_local() as session:
            session.execute(sql_statement)
            session.commit()
