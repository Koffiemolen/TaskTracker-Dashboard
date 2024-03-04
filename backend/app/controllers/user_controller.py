""" User controller module. """
from typing import List
import logging
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserLoginSchema(BaseModel):
    """User login schema."""
    username: str
    password: str


class UserAuthResponse(BaseModel):
    """User authentication response."""
    access_token: str
    token_type: str = "bearer"
    roles: List[str]


# @router.post("/users/login", response_model=UserAuthResponse)
# def login(user: UserLoginSchema):
#     """Authenticate user and return JWT token with roles."""
#     authenticated, roles = authenticate_user(user.username, user.password)
#     logger.info("Authenticated: %s, Roles: %s", authenticated, roles)
#     if authenticated:
#         access_token = create_access_token(data={"sub": user.username, "roles": roles})
#         return {"access_token": access_token, "token_type": "bearer", "roles": roles}
#     raise HTTPException(status_code=401, detail="Invalid username or password")
