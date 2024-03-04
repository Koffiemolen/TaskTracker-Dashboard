"""
This module contains the database router for the FastAPI application.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from backend.app.services.automate_database_service import DatabaseService  # pylint: disable=import-error
from backend.app.models.workflow_link_construct import WorkflowLinkConstruct  # pylint: disable=import-error

router = APIRouter()


@router.get("/data")
async def get_data(db_service: DatabaseService = Depends(DatabaseService)):
    """
    An endpoint which uses a DatabaseService Dependency to fetch data from the
    [Automate11].[dbo].[workflowlinkconstructs] and returns them.
    """
    data = await db_service.fetch_data("SELECT * FROM [Automate11].[dbo].[workflowlinkconstructs]")
    return {"data": data}


@router.get("/workflow-links/", response_model=List[WorkflowLinkConstruct])
def read_workflow_links():
    """
    An endpoint that returns a list of WorkflowLinkConstruct objects. If an exception occurs
    during the data fetching process, it throws HTTPException with status code 500.
    """
    try:
        workflow_links = DatabaseService.fetch_workflow_link_constructs()
        return workflow_links
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
