""" This module contains the DatabaseService class, which is a service for
managing and interacting with the database. """
import os
from sqlalchemy import text, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError



class TaskTrackerDatabaseService:  # pylint: disable=too-few-public-methods
    """
    A service for managing and interacting with the database.
    """

    DATABASE_URL = os.getenv('TASKTRACKER_DB_CONNECTION_STRING')
    # Create an engine instance
    engine = create_engine(DATABASE_URL, echo=True)

    @classmethod
    def get_enriched_tasks(cls, workflow_id: str):
        """
        Retrieve all tasks for a specific workflow.
        """
        try:
            query = text("""
SELECT task.*
	,agents.AgentName AS AgentName
	,agents.GroupResourceID AS AgentGroupResourceID
	,agents.GroupName AS AgentGroupName
	,agents.Notes AS AgentNotes
	,agents.Enabled AS AgentEnabled
	,agents.RowUpdated AS AgentRowUpdated
	,trig.TriggerName AS TriggerName
	,trig.TriggerType AS TriggerType
	,trig.Source AS TriggerSource
	,trig.ScheduleType AS TriggerScheduleType
	,trig.LastLaunchDate AS TriggerLastLaunchDate
	,trig.NextLaunchDate AS TriggerNextLaunchDate
	,trig.Frequency AS TriggerFrequency
	,trig.RowUpdatedOn AS TriggerRowUpdatedOn
FROM [TaskTracker].[dbo].[tasks] AS task
LEFT JOIN TaskTracker.dbo.agents AS agents ON agents.AgentID = task.AgentID
LEFT JOIN [TaskTracker].[dbo].[triggers] AS trig ON trig.triggerID = task.ConstructID
WHERE task.WorkflowID = :workflow_id;
              """)
            with Session(bind=cls.engine) as session:
                result = session.execute(query, params={"workflow_id": workflow_id})
                return list(result.mappings().all())
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            # Handle the error, e.g., by logging or by returning a custom error message
            return []
