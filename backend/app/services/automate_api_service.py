"""
This module is designed to facilitate API interactions with Automate.
It provides an interface for fetching data from the API which includes
workflow data, agent data, and user data. Environment variables are used for
authentication purpose.
"""

import base64
import os
import logging
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AutomateAPIService:
    """
    A service to automate interactions with the Automate API.

    Attributes
    ---------
    base_url : str
    An endpoint URL at which the API is expected to be hosted.

    username : str
    A username used for API authentication.

    password : str
    A password associated with the username for API authentication.

    auth_header : str
    The Basic Authorization header used for API authentication.
    """

    def __init__(self):
        self.base_url = os.getenv("AUTOMATE_API_BASE_URL")
        self.username = os.getenv("AUTOMATE_API_USERNAME")
        self.password = os.getenv("AUTOMATE_API_PASSWORD")
        self.auth_header = self._generate_auth_header()

    def _generate_auth_header(self) -> str:
        """
        Generate the Basic Authorization header.

        Returns
        ------
        The Basic Authorization header in format 'Basic {encoded_credentials}'
        """
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"

    async def get_workflow_data(self) -> dict:
        """
        Fetch workflow data from the Automate API asynchronously.

        Returns
        ------
        The response of the API in the JSON format.

        Exception
        ------
        Raises HTTPException on http status error.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/agents/list",
                    headers={
                        "Accept": "application/json",
                        "Authorization": self.auth_header
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e)) from e

    async def get_agents_list(self) -> dict:
        """
        Fetch agent data from the Automate API asynchronously.

        Returns
        ------
        The response of the API in the JSON format.

        Exception
        ------
        Raises HTTPException on http status error.
        """
        async with httpx.AsyncClient() as client:
            try:
                logger.info("Fetching agents list")
                logger.info("Base URL: %s", self.base_url)
                response = await client.get(
                    f"{self.base_url}/agents/list",
                    headers={
                        "Accept": "application/json",
                        "Authorization": self.auth_header
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e)) from e

    async def get_users_list(self) -> dict:
        """
        Fetch user data from the Automate API asynchronously.

        Returns
        ------
        The response of the API in the JSON format.

        Exception
        ------
        Raises HTTPException on http status error.
        """
        async with httpx.AsyncClient() as client:
            try:
                logger.info("Fetching agents list")
                logger.info("Base URL: %s", self.base_url)
                response = await client.get(
                    f"{self.base_url}/users/list",
                    headers={
                        "Accept": "application/json",
                        "Authorization": self.auth_header
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=e.response.status_code, detail=str(e)) from e


# Example usage within an async route in FastAPI
# from fastapi import FastAPI, Depends
# app = FastAPI()
#
# async def get_automate_api_service() -> AutomateAPIService:
#     return AutomateAPIService()
#
# @app.get("/workflows")
# async def workflows(automate_api_service: AutomateAPIService = Depends(get_automate_api_service)):
#     return await automate_api_service.get_workflow_data()
