# /backend/app/services/workflow_service.py
""" This module contains the workflow service. """
import os

from sqlalchemy.orm import Session
import requests
from requests.auth import HTTPBasicAuth
from backend.app.models.workflow_model import Workflow  # pylint: disable=import-error

# read environment variables
AUTOMATE_USERNAME = os.getenv("AUTOMATE_USERNAME")
AUTOMATE_PASSWORD = os.getenv("AUTOMATE_PASSWORD")
AUTOMATE_HOST = os.getenv("AUTOMATE_HOST")
AUTOMATE_PORT = os.getenv("AUTOMATE_PORT")


class WorkflowService:
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

    def run_automate_workflow(self, workflow_id: str) -> dict:
        """
        Run a workflow by id using Automate API.
        :param workflow_id:
        :return: Workflow execution result
        """
        url = self._construct_automate_url(workflow_id)  # extract URL construction logic
        print("Url: ", url)
        result = None
        try:
            response = requests.post(url, auth=HTTPBasicAuth(AUTOMATE_USERNAME, AUTOMATE_PASSWORD),
                                     timeout=5)  # pylint: disable=line-too-long
            print("Response: ", response)
            result = self._construct_response(response)  # extract response handling logic
        except requests.exceptions.Timeout:
            print("Timeout occurred")
            # return a value when an exception occurs
            result = {"error": "Timeout occurred"}

        return result

    def _construct_automate_url(self, workflow_id):
        """Constructs a URL for Automate API."""
        url = (
            f"http://{AUTOMATE_USERNAME}:{AUTOMATE_PASSWORD}@"
            f"{AUTOMATE_HOST}:{AUTOMATE_PORT}/"
            f"BPAManagement/workflows/{workflow_id}/run"
        )
        return url

    def _construct_response(self, response):
        """Constructs a response dict based on HTTP response."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            err_response = {
                "Result": "error",
                "Info": str(e),
                "Data": None
            }
            if response.status_code:
                err_response['Info'] = f"HTTP error {response.status_code}"
            return err_response
