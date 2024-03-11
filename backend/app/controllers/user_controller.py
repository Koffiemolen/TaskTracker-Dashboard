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
