"""
This module contains Automate API Endpoints for 'agents' and 'users'.
Each endpoint is protected and requires the user to have the 'admin' role for access.
If a user without the 'admin' role tries to access any of these endpoints, an HTTP Exception with a
403 status code is raised.

Author: Bastiaan Clement
Version: 1.0
"""

from fastapi import APIRouter, Depends
from backend.app.services.automate_api_service import AutomateAPIService  # pylint: disable=import-error
from backend.app.dependencies.dependencies import require_role # pylint: disable=import-error

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
