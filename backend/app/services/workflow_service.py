# workflow_service.py
""" This module contains the workflow service. """

from sqlalchemy.orm import Session
from backend.app.models.workflow_model import Workflow  # pylint: disable=import-error


class WorkflowService:  # pylint: disable=too-few-public-methods
    """ A class representing the workflow service.
    """
    def __init__(self, db: Session):
        self.db = db

    def get_all_workflows(self):
        """
        Retrieve all workflows from the database.

        Returns:
            A list of all Workflow instances stored in the database.
        """
        return self.db.query(Workflow).all()
