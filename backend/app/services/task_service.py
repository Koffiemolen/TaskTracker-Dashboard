# workflow_service.py
""" This module contains the task service. """
from typing import List
from sqlalchemy.orm import Session
from backend.app.models.task_model import Task  # pylint: disable=import-error
from backend.app.schemas.task_enriched_schema import TaskEnrichedSchema  # pylint: disable=import-error
from backend.app.services.tasktracker_database_service import TaskTrackerDatabaseService  # pylint: disable=import-error


class TaskService:  # pylint: disable=too-few-public-methods
    """ A class representing the task service.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all_tasks(self):
        """
        Retrieve all workflows from the database.

        Returns:
            A list of all Workflow instances stored in the database.
        """
        return self.db.query(Task).all()

    def get_enriched_tasks(self, workflow_id: str) -> List[TaskEnrichedSchema]:
        """
        :param workflow_id:
        :return:
        """
        # Use the TaskTrackerDatabaseService to fetch data
        tasks_data = TaskTrackerDatabaseService.get_enriched_tasks(workflow_id)
        # Convert the data to Pydantic models or other desired format
        return [TaskEnrichedSchema.model_validate(task) for task in tasks_data]
