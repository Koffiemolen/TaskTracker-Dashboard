"""
This module provides the `get_current_user` function to extract the username
from a valid token provided by a user. It relies on the FastAPI OAuth2 security model
and the PyJWT library for token decoding and validation.

If the token is invalid or the "sub" field (representing the username)
does not exist in the payload, it raises an HTTP 401 Unauthorized exception.

Required Environment Variables:
    - JWT_SECRET_KEY: The secret key to decode JWT
    - JWT_ALGORITHM: The algorithm used for encoding JWT

Dependencies:
    - fastapi
    - fastapi.security
    - jwt
    - os
    - logging
"""

from os import getenv
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
