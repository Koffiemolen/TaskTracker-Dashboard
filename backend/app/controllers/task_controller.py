""" This module contains the task controller. """
from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend.app.schemas.task_schema import TaskSchema  # pylint: disable=import-error
from backend.app.dependencies.dependencies import get_db  # pylint: disable=import-error
from backend.app.services.task_service import TaskService  # pylint: disable=import-error
from backend.app.schemas.task_enriched_schema import TaskEnrichedSchema  # pylint: disable=import-error

router = APIRouter()


@router.get("/list-all", response_model=List[TaskSchema])
def list_all_workflows(db: Session = Depends(get_db)):
    """
    List all workflows.

    Args:
        db: The database session to use for querying the workflows.

    Returns:
        A list of all workflows stored in the database.
    """
    task_service = TaskService(db)
    tasks = task_service.get_all_tasks()
    return tasks


@router.get("/enriched/{workflow_id}", response_model=List[TaskEnrichedSchema])
def get_enriched_tasks_for_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """
    :param workflow_id:
    :param db:
    :return:
    """
    task_service = TaskService(db)
    return task_service.get_enriched_tasks(workflow_id)
