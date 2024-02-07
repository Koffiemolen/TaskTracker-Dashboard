"""
This module provides a function to authenticate a user against an Active
Directory (AD) server using NTLM authentication.

Usage:

    authenticate_user(username, password)

    This attempts to connect to the AD server specified as an environment variable with the provided username   # pylint: disable=line-too-long
    and password.
    The user is authenticated if the connection is successful; otherwise an exception is captured and logged,   # pylint: disable=line-too-long
    and False is returned.

Module Dependencies:
    ldap3, os, logging

Environment Variables:
    AD_SERVER : The AD server's address
    AD_DOMAIN : The AD domain
    AD_SEARCH_BASE : The search base in the AD
"""
import os
import logging
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.core.exceptions import LDAPExceptionError, LDAPBindError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user against an AD server with NTLM authentication.

    Args:
    username (str): The username of the user to authenticate
    password (str): The user's password

    Returns:
    A boolean indicating success or failure. True if the user is authenticated; False if authentication fails or   # pylint: disable=line-too-long
    an error occurs.
    """
    server = Server(os.getenv("AD_SERVER"), get_info=ALL)
    domain = os.getenv("AD_DOMAIN")

    try:
        conn = Connection(server, user=f"{domain}\\{username}", password=password,
                          authentication=NTLM)  # pylint: disable=line-too-long
        print(f"Connection: {conn}")
        if not conn.bind():
            return False
        # Optionally search for user details in AD here
        return True
    except (LDAPExceptionError, LDAPBindError) as e:
        print(f"An error occurred while connecting to AD: {e}")  # pylint: disable=broad-except
        return False
