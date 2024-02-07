from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import timedelta
from backend.app.services.authentication_service import authenticate_user
from backend.app.services.token_service import create_access_token
from backend.app.dependencies.dependencies import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class UserLoginSchema(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(user: UserLoginSchema):
    print(f"User: {user.username}, Password: {user.password}")
    logger.info(f"User: {user.username}, Password: {user.password}")
    # Authenticate the user
    if not authenticate_user(user.username, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Generate a token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Return the token
    print(f"Token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected-endpoint")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected endpoint", "user": current_user}
