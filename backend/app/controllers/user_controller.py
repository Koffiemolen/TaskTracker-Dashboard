""" User controller module. """
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.authentication_service import authenticate_user  # pylint: disable=import-error

router = APIRouter()


class UserLoginSchema(BaseModel):
    """User login schema."""
    username: str
    password: str


@router.post("/users/login")
def login(user: UserLoginSchema):
    """Authenticate user."""
    print(f"Authenticating user {user.username}")
    if authenticate_user(user.username, user.password):
        return {"message": "User authenticated successfully"}
    raise HTTPException(status_code=401, detail="Invalid username or password")
