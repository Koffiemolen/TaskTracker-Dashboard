"""
This module contains API routes for auth module.

It includes:
1. A login endpoint
2. A protected endpoint
"""
import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.app.services.authentication_service import authenticate_user  # pylint: disable=import-error
from backend.app.services.token_service import create_access_token  # pylint: disable=import-error
from backend.app.dependencies.dependencies import get_current_user_roles  # pylint: disable=import-error
from backend.app.dependencies.dependencies import require_role # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class UserLoginSchema(BaseModel):
    """
    Pydantic model for User Login.
    """
    username: str
    password: str


@router.post("/login")
def login(user: UserLoginSchema):
    """Login endpoint to authenticate user and generate JWT token.

    Args:
        user (UserLoginSchema): The user login request with username and password.

    Raises:
        HTTPException: If user authentication failed.

    Returns:
        dict : Returns an active JWT token
    """
    logger.info("Checking if password and user exists in AD, checking user: %s", user.username)
    authenticated, roles = authenticate_user(user.username, user.password)
    logger.info("Authenticated: %s, Roles: %s", authenticated, roles)
    if authenticated:
        access_token = create_access_token(data={"sub": user.username, "roles": roles})
        return {"access_token": access_token, "token_type": "bearer", "roles": roles}

    raise HTTPException(status_code=401, detail="Invalid username or password")


# @router.get("/protected-endpoint")
# async def protected_endpoint(current_user: dict = Depends(get_current_user)):
#     return {"message": "This is a protected endpoint", "user": current_user}

@router.get("/protected-endpoint", dependencies=[Depends(require_role("admin"))])
async def protected_endpoint():
    """Protected endpoint for authenticated users."""
    return {"message": "You have access to the admin endpoint."}


@router.get("/admin-only")
def admin_only_endpoint(roles=Depends(require_role("admin"))):  # pylint: disable=unused-argument
    """Admin only endpoint."""
    return {"message": "Welcome, admin!"}


@router.get("/test-roles")
def test_roles(roles: List[str] = Depends(get_current_user_roles)):
    """Test roles endpoint."""
    return {"roles": roles}
