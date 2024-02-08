"""
This module contains API routes for auth module.

It includes:
1. A login endpoint
2. A protected endpoint
"""
import logging
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.app.services.authentication_service import authenticate_user  # pylint: disable=import-error
from backend.app.services.token_service import create_access_token  # pylint: disable=import-error
from backend.app.dependencies.dependencies import get_current_user  # pylint: disable=import-error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class UserLoginSchema(BaseModel):
    """
    Pydantic model for User Login.

    Attributes:
        username (str): username of user
        password (str): password of user
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
    print(f"User: {user.username}, Password: {user.password}")
    logger.info("User: %s", user.username)

    if not authenticate_user(user.username, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    print(f"Token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-endpoint")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """Protected endpoint which return some protected data.

    Args:
        current_user (dict): The username of current logged-in user retrieved through JWT token.

    Returns:
        dict : Return some message along with user data.
    """
    return {"message": "This is a protected endpoint", "user": current_user}
