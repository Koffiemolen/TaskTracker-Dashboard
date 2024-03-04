"""This module contains dependencies for user authentication and role-based access control."""
import logging
from os import getenv
from typing import List
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.app.database import SessionLocal  # pylint: disable=import-error

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Dependency
def get_db():
    """
    Get a database session.

    :return: A database session.
    :rtype: Generator[Session, None, None]
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Function for getting the current user from a valid token.

    This function extracts username from the token's payload.
    If the token is not valid or the username does not exist,
    it raises an HTTP 401 Unauthorized exception.

    Args:
        token (str): A string representing the token received from the user.
        Default is a token provided by the FastAPI dependency `oauth2_scheme`.

    Raises:
        HTTPException(401): If the token is invalid, or if the "sub" field (representing the username)  # pylint: disable=line-too-long
        does not exist in the payload.

    Returns:
        dict: A dict mapping "username" to username, if the token is valid and the username exists.
    """

    try:
        payload = jwt.decode(token, getenv("JWT_SECRET_KEY"), algorithms=[getenv("JWT_ALGORITHM")])
        username: str = payload.get("sub")
        print(f"Username: {username}")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid authentication credentials")  # pylint: disable=line-too-long
        return {"username": username}
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials") from exc


def get_current_user_roles(token: str = Depends(oauth2_scheme)) -> List[str]:
    """Extract user roles from JWT token."""
    try:
        payload = jwt.decode(token, getenv("JWT_SECRET_KEY"), algorithms=[getenv("JWT_ALGORITHM")])
        roles: List[str] = payload.get("roles", [])
        logger.info("Extracted roles in get_current_user_roles: %s", roles)
        return roles
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials") from exc


def require_role(required_role: str):
    """Dependency to enforce role-based access control."""

    def role_checker(roles: List[str] = Depends(get_current_user_roles)):
        logger.info("Roles: %s", roles)
        if required_role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Insufficient permissions")  # pylint: disable=line-too-long

    return role_checker
