"""This module contains dependencies for user authentication and role-based access control."""
import os
import logging
from ldap3 import Server, Connection, ALL, NTLM
from ldap3.core.exceptions import LDAPExceptionError, LDAPBindError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_cn(dn):
    """Extract the CN value from a distinguished name (DN)."""
    return dn.split(',')[0][3:]  # Extracts the CN value from the DN


def authenticate_user(username: str, password: str) -> (bool, list):
    """
    Authenticate a user against an AD server with NTLM authentication and fetch user roles.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The user's password.

    Returns:
        A tuple containing a boolean indicating success or failure, and a list of roles.
    """
    server = Server(os.getenv("AD_SERVER"), get_info=ALL)
    domain = os.getenv("AD_DOMAIN")
    roles = []

    def is_member(value, iterable):
        for item in iterable:
            logger.info("Checking if %s is in %s", value, item)
            if value is item or value == item:
                return True
        return False

    try:
        conn = Connection(server, user=f"{domain}\\{username}", password=password, authentication=NTLM)  # pylint: disable=line-too-long
        if not conn.bind():
            return False, roles

        # Search for user's group memberships
        search_base = os.getenv("AD_SEARCH_BASE")
        search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
        conn.search(search_base, search_filter, attributes=['memberOf'])

        # Define the CNs of the groups you're interested in
        admin_group_cn = extract_cn("CN=TaskTracker-Dashboard-Admins,OU=Contoso Groups,DC=contoso,DC=local")  # pylint: disable=line-too-long
        user_group_cn = extract_cn("CN=TaskTracker-Dashboard-Users,OU=Contoso Groups,DC=contoso,DC=local")  # pylint: disable=line-too-long

        if conn.entries:
            user_groups = conn.entries[0].memberOf
            # Extract CNs from user_groups
            user_group_cns = [extract_cn(group) for group in user_groups]
            logger.info("User is member of (CNs): %s", user_group_cns)

            logger.info("Is user a member of admin group? %s", is_member(admin_group_cn, user_group_cns))  # pylint: disable=line-too-long

            # Check for specific group CNs to determine roles
            logger.info("Old check: Checking if user %s is an admin or a user...", username)
            if admin_group_cn in user_group_cns:
                logger.info("User %s is an admin", username)
                roles.append("admin")
            if user_group_cn in user_group_cns:
                logger.info("User %s is a user", username)
                roles.append("user")

            logger.info("Roles: %s", roles)
        return True, roles
    except (LDAPExceptionError, LDAPBindError) as e:
        logger.error("An error occurred while connecting to AD: %s", e)
        return False, []
