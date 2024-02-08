"""
This module is used for creating JWT access token with a certain expiring time.

The main libraries used in this module are:
    - jwt: for encoding and decoding JWT tokens
    - datetime: for handling and operating with date and time
    - os: for getting environment variables
    - logging: for logging events and errors

"""

from datetime import datetime, timedelta
from os import getenv
import logging
import jwt
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with a certain expiring time.

    :param data: a dictionary containing the data to be included in the JWT
    :type data: dict
    :param expires_delta: time duration for the token to expire. Defaults to 15 mins
    :type expires_delta: timedelta, optional
    :return: a JWT access token
    :rtype: str

    """
    print(f"Creating access token for {data}")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv("JWT_SECRET_KEY"), algorithm=getenv("JWT_ALGORITHM"))
    return encoded_jwt
