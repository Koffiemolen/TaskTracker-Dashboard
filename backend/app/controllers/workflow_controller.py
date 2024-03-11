""" This module contains the workflow controller. """
from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend.app.schemas.workflow_schema import WorkflowSchema  # pylint: disable=import-error
from backend.app.dependencies.dependencies import get_db  # pylint: disable=import-error
from backend.app.services.workflow_service import WorkflowService  # pylint: disable=import-error


router = APIRouter()


@router.get("/list-all", response_model=List[WorkflowSchema])
def list_all_workflows(db: Session = Depends(get_db)):
    """
    List all workflows.

    Args:
        db: The database session to use for querying the workflows.

    Returns:
        A list of all workflows stored in the database.
    """
    workflow_service = WorkflowService(db)
    workflows = workflow_service.get_all_workflows()
    return workflows
