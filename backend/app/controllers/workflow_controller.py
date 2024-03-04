# workflow_controller.py
"""
This module contains the router and endpoint definitions for managing workflows.
"""
from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from backend.app.models.workflow_model import Workflow  # pylint: disable=import-error
from backend.app.schemas.workflow_schema import WorkflowSchema  # pylint: disable=import-error
from backend.app.dependencies.dependencies import get_db  # pylint: disable=import-error

bearer_scheme = HTTPBearer()
router = APIRouter()


@router.get("/list")
def read_workflows():
    """Fetches and returns the list of workflows

    This endpoint fetches and returns a list of existing workflows.

    Returns:
        dict: A dictionary with a list of workflows.
    """

    # Logic to fetch and return workflow data
    return {"workflows": ["workflow1", "workflow2"]}


@router.get("/list-all", response_model=List[WorkflowSchema])
def list_all_workflows(db: Session = Depends(get_db), token: str = Depends(bearer_scheme)):  # pylint: disable=unused-argument
    """
    :param db: The database session to use for querying the workflows.
    :param token: The security token used for authentication.
    :return: A list of all workflows stored in the database.

    """
    workflows = db.query(Workflow).all()
    return workflows
