# /backend/app/routers/automateapi_router.py
"""
This module contains Automate API Endpoints for 'agents' and 'users'.
Each endpoint is protected and requires the user to have the 'admin' role for access.
If a user without the 'admin' role tries to access any of these endpoints, an HTTP Exception with a
403 status code is raised.

Author: Bastiaan Clement
Version: 1.0
"""
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from backend.app.services.automate_api_service import AutomateAPIService  # pylint: disable=import-error
from backend.app.dependencies.dependencies import require_role  # pylint: disable=import-error
from backend.app.services.workflow_service import WorkflowService  # pylint: disable=import-error
from backend.app.dependencies.dependencies import get_db  # pylint: disable=import-error

router = APIRouter()


@router.get("/agents")
async def get_agents(automate_service: AutomateAPIService = Depends(AutomateAPIService),
                     roles=Depends(require_role("admin"))):  # pylint: disable=unused-argument
    """
    This function gets the list of agents from the Automate API Service.
    If the user doesn't have the 'admin' role, an HTTP Exception with a 403
    status code is raised.

    :param automate_service: An instance of the AutomateAPIService.
    :type automate_service: AutomateAPIService
    :param roles: A list of roles which permit access to this endpoint.
    :type roles: depends on
    :return: A list of agents.
    """
    return await automate_service.get_agents_list()


@router.get("/users")
async def get_users_list(automate_service: AutomateAPIService = Depends(AutomateAPIService),
                         roles=Depends(require_role("admin"))):  # pylint: disable=unused-argument
    """
    This function gets the list of users from the Automate API Service.
    If the user doesn't have the 'admin' role, an HTTP Exception with a 403
    status code is raised.

    :param automate_service: An instance of the AutomateAPIService.
    :type automate_service: AutomateAPIService
    :param roles: A list of roles which permit access to this endpoint.
    :type roles: Depends on
    :return: A list of users.
    """
    return await automate_service.get_users_list()


@router.post("/workflows/{workflow_id}/run")
# async def run_workflow(workflow_id: str, roles=Depends(require_role("admin"))):
async def run_workflow(workflow_id: str, db: Session = Depends(get_db)):
    """
    Run a workflow by id using Automate API.
    If the user doesn't have the 'admin' role, an HTTP Exception with a 403
    status code is raised.

    :param workflow_id: The id of the workflow to run.
    :type workflow_id: str
    """
    try:
        workflow_service = WorkflowService(db)
        result = workflow_service.run_automate_workflow(workflow_id)
        if result["Result"] == "success":
            return result
        if result["Result"] == "failure":
            raise HTTPException(status_code=400, detail=result["Info"])
        else:
            raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
